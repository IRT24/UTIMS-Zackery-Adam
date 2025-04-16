from django.contrib import admin
from .models import InventoryItem, Category  # Import your models

admin.site.register(InventoryItem)
admin.site.register(Category)