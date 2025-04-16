from django import forms
from .models import InventoryItem, Category

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'quantity', 'price_per_unit', 'low_stock_threshold']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per unit'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter low stock threshold'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all categories or create default ones if none exist
        categories = Category.objects.all()
        if not categories.exists():
            # Create some default categories
            default_categories = ['Electronics', 'Office Supplies', 'Furniture', 'Food', 'Other']
            for category_name in default_categories:
                Category.objects.get_or_create(name=category_name)
            
            # Refresh the categories
            categories = Category.objects.all()
        
        # Set category choices
        self.fields['category'].queryset = categories
        
        # Add "empty" option to allow user to see choices
        self.fields['category'].empty_label = "-- Select Category --" 