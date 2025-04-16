from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
import datetime
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, UserEditForm
from .models import CustomUser, UserActivity
from .decorators import admin_required, validate_input

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    @validate_input()
    def dispatch(self, request, *args, **kwargs):
        # Check if the account is locked - only for POST requests
        if request.method == 'POST' and hasattr(request, 'POST'):
            username = request.POST.get('username', '')
            if username:
                # Use consistent cache key naming - same as in form_invalid
                cache_key = f"failed_login:{username}"
                failed_attempts = cache.get(cache_key, 0)
                
                # If login attempts exceed max attempts, check lock duration
                max_attempts = getattr(settings, 'ACCOUNT_LOCKOUT_ATTEMPTS', 5)
                if failed_attempts >= max_attempts:
                    # Get lockout timestamp - use the same key as in form_invalid
                    lockout_timestamp = cache.get(f"account_lockout:{username}")
                    if lockout_timestamp:
                        # Calculate remaining lockout time
                        current_time = timezone.now()
                        lockout_duration = getattr(settings, 'ACCOUNT_LOCKOUT_TIME', 300)  # Default 5 minutes
                        time_elapsed = (current_time - lockout_timestamp).total_seconds()
                        time_remaining = lockout_duration - time_elapsed
                        
                        if time_remaining > 0:
                            # Account still locked
                            minutes = int(time_remaining // 60)
                            seconds = int(time_remaining % 60)
                            messages.error(
                                request, 
                                _(f"Account locked due to multiple failed login attempts. "
                                  f"Please try again in {minutes} minutes and {seconds} seconds.")
                            )
                            return self.render_to_response(self.get_context_data())
                        else:
                            # Lockout period expired, reset counter
                            cache.delete(cache_key)
                            cache.delete(f"account_lockout:{username}")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # Special handling for GET requests to clear HSTS header
        response = super().get(request, *args, **kwargs)
        # Add clear HSTS header to help with browser HTTPS issues
        response['Strict-Transport-Security'] = 'max-age=0'
        return response
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        # Check if cleaned_data exists and contains username
        if not hasattr(form, 'cleaned_data') or not form.cleaned_data:
            return super().form_valid(form)
            
        username = form.cleaned_data.get('username')
        if not username:
            return super().form_valid(form)
            
        # Check if account is locked
        lockout_timestamp = cache.get(f"account_lockout:{username}")
        if lockout_timestamp:
            # Account is locked, check if the lockout period is still active
            current_time = timezone.now()
            lockout_time = getattr(settings, 'ACCOUNT_LOCKOUT_TIME', 300)
            time_elapsed = (current_time - lockout_timestamp).total_seconds()
            
            if time_elapsed < lockout_time:
                # Account is still locked
                time_remaining = lockout_time - time_elapsed
                minutes = int(time_remaining // 60)
                seconds = int(time_remaining % 60)
                messages.error(
                    self.request, 
                    _(f"Account locked due to multiple failed login attempts. "
                      f"Please try again in {minutes} minutes and {seconds} seconds.")
                )
                return self.form_invalid(form)
            else:
                # Lockout period expired, clear the lockout
                cache.delete(f"account_lockout:{username}")
        
        # Clear any previous failed login attempts for this user
        cache_key = f"failed_login:{username}"
        cache.delete(cache_key)
        
        # Session always expires when browser closes for enhanced security
        self.request.session.set_expiry(0)
        
        response = super().form_valid(form)
        
        # Create login activity record
        UserActivity.objects.create(
            user=self.request.user,
            action='login',
            ip_address=self.get_client_ip()
        )
        
        # Clear HSTS header from response
        response['Strict-Transport-Security'] = 'max-age=0'
        
        return response
    
    def form_invalid(self, form):
        """Handle invalid credentials with account lockout."""
        # Check if cleaned_data exists and contains username
        if not hasattr(form, 'cleaned_data') or not form.cleaned_data:
            return super().form_invalid(form)
        
        username = form.cleaned_data.get('username')
        if not username:
            return super().form_invalid(form)
            
        # Skip lockout for invalid usernames to prevent username enumeration
        if not CustomUser.objects.filter(username=username).exists():
            return super().form_invalid(form)
        
        # Check if account is already locked
        lockout_timestamp = cache.get(f"account_lockout:{username}")
        if lockout_timestamp:
            # Account is already locked, check if the lockout period is still active
            current_time = timezone.now()
            lockout_time = getattr(settings, 'ACCOUNT_LOCKOUT_TIME', 300)
            time_elapsed = (current_time - lockout_timestamp).total_seconds()
            
            if time_elapsed < lockout_time:
                # Account is still locked
                time_remaining = lockout_time - time_elapsed
                minutes = int(time_remaining // 60)
                seconds = int(time_remaining % 60)
                messages.error(
                    self.request, 
                    _(f"Account locked due to multiple failed login attempts. "
                      f"Please try again in {minutes} minutes and {seconds} seconds.")
                )
                return super().form_invalid(form)
        
        # Increment failed login attempts
        cache_key = f"failed_login:{username}"
        failed_attempts = cache.get(cache_key, 0) + 1
        
        # Set expiry based on settings or default to 5 minutes (300 seconds)
        lockout_time = getattr(settings, 'ACCOUNT_LOCKOUT_TIME', 300)
        max_attempts = getattr(settings, 'ACCOUNT_LOCKOUT_ATTEMPTS', 5)
        
        if failed_attempts >= max_attempts:
            # Account is locked
            messages.error(
                self.request, 
                f"Account locked due to multiple failed attempts. Try again in {lockout_time // 60} minutes."
            )
            # Store lockout timestamp to check time remaining on future attempts
            cache.set(f"account_lockout:{username}", timezone.now(), lockout_time)
            # Make sure to keep the failed attempts counter during the lockout period
            cache.set(cache_key, failed_attempts, lockout_time)
        else:
            # Store failed attempt count with the same expiry as the lockout
            cache.set(cache_key, failed_attempts, lockout_time)
            messages.warning(
                self.request,
                f"Invalid credentials. {max_attempts - failed_attempts} attempts remaining before account lockout."
            )
        
        return super().form_invalid(form)
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

class CustomLogoutView(LogoutView):
    next_page = 'login'
    http_method_names = ['get', 'post']  # Allow both GET and POST requests
    
    def dispatch(self, request, *args, **kwargs):
        # Record logout activity before the user is logged out
        if request.user.is_authenticated:
            UserActivity.objects.create(
                user=request.user,
                action='logout',
                ip_address=self.get_client_ip(request)
            )
        return super().dispatch(request, *args, **kwargs)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    success_url = '/dashboard/'
    
    @validate_input()
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        
        # Add success message
        messages.success(self.request, f'Account created for {user.username}! You can now log in.')
        
        # Redirect to login instead of auto-login
        return redirect('login')

# Admin-only views for user management
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('home')

class UserListView(AdminRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add user activities to the context
        context['user_activities'] = UserActivity.objects.all().select_related('user').order_by('-timestamp')[:20]
        return context
        
    def get(self, request, *args, **kwargs):
        # Completely clear all messages before rendering the page
        storage = messages.get_messages(request)
        # Iterate through and mark all existing messages as used
        for message in storage:
            pass  # Simply iterating marks them as read
        
        # Now the storage is empty and no messages will be displayed
        return super().get(request, *args, **kwargs)

class UserCreateView(AdminRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')
    
    @validate_input()
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_add'] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "New user has been created successfully!")
        return super().form_valid(form)

class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserEditForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')
    
    def form_valid(self, form):
        messages.success(self.request, f"User {form.instance.username} has been updated successfully.")
        return super().form_valid(form)

class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        messages.success(request, f"User {user.username} has been deleted successfully.")
        return super().delete(request, *args, **kwargs)

@login_required
@admin_required
def toggle_user_role(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    
    # Toggle the role
    if user.role == 'admin':
        user.role = 'employee'
        message = f"{user.username}'s role changed to Employee"
    else:
        user.role = 'admin'
        message = f"{user.username}'s role changed to Admin"
    
    user.save()
    messages.success(request, message)
    return HttpResponseRedirect(reverse('users:list'))

@login_required
def extend_session(request):
    """View to handle requests to extend the user's session"""
    if request.method != 'POST':
        # Only allow POST requests for session extension
        return HttpResponseForbidden("Only POST requests are allowed.")
        
    # Update the session's last_activity timestamp
    request.session['last_activity'] = timezone.now().isoformat()
    
    # Save the session explicitly to ensure it's updated
    request.session.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'timestamp': request.session['last_activity']})
    
    # For non-AJAX requests, redirect back to the referring page or home
    next_url = request.META.get('HTTP_REFERER', reverse('home'))
    return HttpResponseRedirect(next_url) 