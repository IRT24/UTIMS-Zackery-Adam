from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_dashboard, name='dashboard'),
    path('inventory/<str:format>/', views.download_inventory_report, name='inventory'),
    path('tasks/<str:format>/', views.download_tasks_report, name='tasks'),
    path('expenses/<str:format>/', views.download_expenses_report, name='expenses'),
] 