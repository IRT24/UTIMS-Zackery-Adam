from django.urls import path
from .views import (
    SignUpView,
    UserListView, 
    UserCreateView,
    UserUpdateView, 
    UserDeleteView,
    toggle_user_role,
    extend_session
)

app_name = 'users'  # For namespacing user management URLs

urlpatterns = [
    # Signup URL (kept for admin-only access via middleware)
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # User management URLs (admin only) - with namespace
    path('', UserListView.as_view(), name='list'),
    path('add/', UserCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
    path('<int:pk>/toggle-role/', toggle_user_role, name='toggle_role'),
    
    # Session management
    path('extend-session/', extend_session, name='extend_session'),
] 