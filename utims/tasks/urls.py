from django.urls import path
from . import views

app_name = "tasks"  # Namespacing the app

urlpatterns = [
    path("", views.TaskListView.as_view(), name="list"),  # The correct URL pattern for tasks
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete'),
]
