from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.conf import settings
import datetime
import time
import re
from django.core.cache import cache
import ipaddress

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Public paths that don't require authentication
        self.public_paths = [
            'login', 'logout',  # signup removed for security
            'password_reset', 'password_reset_done', 
            'password_reset_confirm', 'password_reset_complete',
            'admin:index', 'admin:login'
        ]

    def __call__(self, request):
        # Block access to signup page for security reasons
        url_name = resolve(request.path_info).url_name
        if url_name == 'signup':
            return HttpResponseForbidden("Sign-up is disabled for security reasons. Please contact an administrator.")
            
        # Process request before view is called
        if not request.user.is_authenticated:
            # Check if current URL is in public paths
            is_public = any(url in url_name for url in self.public_paths) if url_name else False
            
            # If URL is not public and user is not authenticated, redirect to login
            if not is_public and not url_name in self.public_paths:
                return redirect('login')
                
        response = self.get_response(request)
        return response 

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get the current timestamp
            current_time = timezone.now()
            
            # Get the last activity time from the session
            last_activity = request.session.get('last_activity')
            
            # Check if we have a last activity time
            if last_activity:
                # Convert the ISO formatted time string back to a datetime object
                last_activity_time = datetime.datetime.fromisoformat(last_activity)
                # Make sure it's timezone aware
                if last_activity_time.tzinfo is None:
                    last_activity_time = timezone.make_aware(last_activity_time)
                
                # Check if the session has timed out (more than 1 minute of inactivity)
                if (current_time - last_activity_time).total_seconds() > 60:  # 1 minute in seconds
                    # Log the user out
                    logout(request)
                    # Add a message to inform the user
                    messages.info(request, "Your session has expired due to inactivity. Please log in again.")
                    # Redirect to login page
                    return redirect('login')
            
            # Update the last activity time for this session
            request.session['last_activity'] = current_time.isoformat()

        response = self.get_response(request)
        return response 

class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to all responses to protect against XSS and other attacks.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy - restricts sources of content to protect against XSS
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "  # 'unsafe-inline' needed for some inline scripts
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "  # For external CSS
            "font-src 'self' https://cdnjs.cloudflare.com; "  # For external fonts
            "img-src 'self' data:; "  # Allow images from same origin and data URIs
            "connect-src 'self'; "  # Restricts where AJAX requests can be made to
            "frame-ancestors 'none'; "  # Prevents your site from being framed (clickjacking protection)
            "form-action 'self'; "  # Restricts where forms can be submitted to
            "base-uri 'self';"  # Restricts use of <base> tag
        )
        
        # X-XSS-Protection - enables browser's built-in XSS filter
        response['X-XSS-Protection'] = '1; mode=block'
        
        # X-Content-Type-Options - prevents MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Referrer-Policy - controls what information is sent in the Referer header
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define rate limits for different endpoints
        self.rate_limits = {
            'login': {'requests': 5, 'window': 60},  # 5 requests per 60 seconds for login
            'api': {'requests': 20, 'window': 60},   # 20 requests per 60 seconds for API
            'default': {'requests': 30, 'window': 60}  # 30 requests per 60 seconds for all other routes
        }
        # Trusted IP ranges (local networks, trusted proxies)
        self.trusted_ips = [
            '127.0.0.1/32',  # Localhost
            '10.0.0.0/8',     # Private network
            '172.16.0.0/12',  # Private network
            '192.168.0.0/16', # Private network
        ]

    def __call__(self, request):
        # Skip rate limiting for trusted IPs
        client_ip = self.get_client_ip(request)
        if self.is_trusted_ip(client_ip):
            return self.get_response(request)

        # Determine the endpoint type for rate limit selection
        path = request.path_info.lstrip('/')
        if path.startswith('login'):
            rate_limit = self.rate_limits['login']
        elif path.startswith('api'):
            rate_limit = self.rate_limits['api']
        else:
            rate_limit = self.rate_limits['default']
        
        # Create a cache key based on IP and endpoint
        cache_key = f"rate_limit:{client_ip}:{path.split('/')[0]}"
        
        # Get current request count and time
        request_history = cache.get(cache_key, {'requests': 0, 'window_start': time.time()})
        
        # Reset counter if the window has expired
        current_time = time.time()
        if current_time - request_history['window_start'] > rate_limit['window']:
            request_history = {'requests': 0, 'window_start': current_time}
        
        # Increment request count
        request_history['requests'] += 1
        
        # Update cache
        cache.set(cache_key, request_history, rate_limit['window'])
        
        # Check if rate limit exceeded
        if request_history['requests'] > rate_limit['requests']:
            return self.rate_limit_exceeded_response(request)
        
        # Add rate limit headers
        response = self.get_response(request)
        response['X-RateLimit-Limit'] = str(rate_limit['requests'])
        response['X-RateLimit-Remaining'] = str(max(0, rate_limit['requests'] - request_history['requests']))
        response['X-RateLimit-Reset'] = str(int(request_history['window_start'] + rate_limit['window']))
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_trusted_ip(self, ip):
        """Check if IP is in trusted IP ranges"""
        client_ip = ipaddress.ip_address(ip)
        for trusted_range in self.trusted_ips:
            if client_ip in ipaddress.ip_network(trusted_range):
                return True
        return False
    
    def rate_limit_exceeded_response(self, request):
        """Return a response when rate limit is exceeded"""
        content = {
            'status': 'error',
            'message': 'Rate limit exceeded. Please try again later.'
        }
        response = HttpResponse(
            '<h1>429 Too Many Requests</h1><p>Rate limit exceeded. Please try again later.</p>',
            content_type='text/html'
        )
        response.status_code = 429
        response['Retry-After'] = '60'  # Try again after 60 seconds
        return response 