from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from users.views import CustomLoginView, CustomLogoutView

@login_required
def home_view(request):
    return render(request, 'home.html')
    
def test_view(request):
    """Simple view to test HTTP access without any redirects or security checks"""
    response = HttpResponse("HTTP Test: If you can see this, HTTP access is working correctly.")
    # Add clear HSTS header to help reset browser settings
    response['Strict-Transport-Security'] = 'max-age=0'
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('inventory:home')),
    path('home/', home_view, name='home'),
    path('inventory/', include('inventory.urls')),  # Inventory module
    path('tasks/', include('tasks.urls')),
    path('expenses/', include('expenses.urls')),
    path('reports/', include('reports.urls')),
    
    # Authentication routes (without namespace)
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # User management routes (with namespace)
    path('accounts/', include('users.urls')),
    
    # Test route for HTTP debugging
    path('http-test/', test_view, name='http_test'),
]

# Add media URL configuration for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
