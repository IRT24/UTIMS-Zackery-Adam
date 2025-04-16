from rest_framework import serializers
from .models import InventoryItem, Category  # Import your models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class InventoryItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Using a nested serializer

    class Meta:
        model = InventoryItem
        fields = ['category', 'name', 'quantity', 'price_per_unit', 'low_stock_threshold']

    def create(self, validated_data):
        category_data = validated_data.pop('category', None)

        # Handle category separately
        if category_data:
            category, _ = Category.objects.get_or_create(**category_data)
        else:
            category = None  # If category is not provided, it remains null

        # Create the InventoryItem
        inventory_item = InventoryItem.objects.create(category=category, **validated_data)
        return inventory_item
