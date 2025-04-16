from django.urls import path
from .views import (
    InventoryListCreateView, 
    InventoryDetailView, 
    low_stock_alert, 
    inventory_list,
    inventory_detail,
    InventoryItemCreateView,
    InventoryItemUpdateView,
    InventoryItemDeleteView,
    CategoryListView
)

app_name = "inventory"  # This allows {% url 'inventory:list' %} to work in base.html

urlpatterns = [
    # Web UI URLs
    path("", inventory_list, name="home"),
    path("inventory/", inventory_list, name="list"),
    path("inventory/<int:pk>/", inventory_detail, name="detail"),
    path("inventory/create/", InventoryItemCreateView.as_view(), name="create"),
    path("inventory/<int:pk>/edit/", InventoryItemUpdateView.as_view(), name="edit"),
    path("inventory/<int:pk>/delete/", InventoryItemDeleteView.as_view(), name="delete"),
    
    # API URLs
    path("api/inventory/", InventoryListCreateView.as_view(), name="api-list"),
    path("api/inventory/<int:pk>/", InventoryDetailView.as_view(), name="api-detail"),
    path("api/categories/", CategoryListView.as_view(), name="api-categories"),
    path("api/low-stock/", low_stock_alert, name="api-low-stock"),
]