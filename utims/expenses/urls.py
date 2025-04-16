from django.urls import path
from . import views

app_name = 'expenses'  # Namespace for the app

urlpatterns = [
    path('', views.ExpenseListView.as_view(), name='list'),  # Matches the expected name
    path('create/', views.ExpenseCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ExpenseDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='delete'),
]
