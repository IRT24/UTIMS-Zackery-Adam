from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import InventoryItem, Category, InventoryLog
from .serializers import InventoryItemSerializer, CategorySerializer
from .forms import InventoryItemForm


# API Views
class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Web UI Views
def inventory_list(request):
    items = InventoryItem.objects.all()
    
    # Get sort parameters
    sort_by = request.GET.get('sort', 'name')  # Default sort by name
    order = request.GET.get('order', 'asc')    # Default ascending order
    
    # Define valid sort fields and their corresponding model fields
    valid_sort_fields = {
        'name': 'name',
        'category': 'category__name',
        'quantity': 'quantity',
        'price': 'price_per_unit',
        'updated': 'last_updated'
    }
    
    # Apply sorting if valid field
    if sort_by in valid_sort_fields:
        order_field = valid_sort_fields[sort_by]
        if order == 'desc':
            order_field = f'-{order_field}'
        items = items.order_by(order_field)
    
    low_stock_items = InventoryItem.objects.filter(quantity__lte=F('low_stock_threshold'))
    low_stock_count = low_stock_items.count()
    
    return render(request, "inventory/inventory_list.html", {
        "inventory_items": items,
        "low_stock_count": low_stock_count,
        "current_sort": sort_by,
        "current_order": order
    })


def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    logs = InventoryLog.objects.filter(item=item).order_by('-timestamp')[:10]
    return render(request, "inventory/inventory_detail.html", {"item": item, "logs": logs})


@api_view(['GET'])
def low_stock_alert(request):
    low_stock_items = InventoryItem.objects.filter(quantity__lte=F('low_stock_threshold'))
    serializer = InventoryItemSerializer(low_stock_items, many=True)
    return Response(serializer.data)


# CRUD Views for Web UI
class InventoryItemCreateView(CreateView):
    model = InventoryItem
    template_name = 'inventory/inventory_form.html'
    form_class = InventoryItemForm
    success_url = reverse_lazy('inventory:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create a log entry
        InventoryLog.objects.create(
            item=self.object,
            action='ADD',
            quantity_changed=self.object.quantity,
            remarks=f"Initial stock created: {self.object.quantity} units"
        )
        return response


class InventoryItemUpdateView(UpdateView):
    model = InventoryItem
    template_name = 'inventory/inventory_form.html'
    form_class = InventoryItemForm
    success_url = reverse_lazy('inventory:list')

    def form_valid(self, form):
        old_quantity = self.get_object().quantity
        response = super().form_valid(form)
        new_quantity = self.object.quantity
        
        # Create a log entry
        quantity_changed = new_quantity - old_quantity
        if quantity_changed != 0:
            action = 'ADD' if quantity_changed > 0 else 'REMOVE'
            InventoryLog.objects.create(
                item=self.object,
                action=action,
                quantity_changed=abs(quantity_changed),
                remarks=f"Updated quantity from {old_quantity} to {new_quantity}"
            )
        
        return response


class InventoryItemDeleteView(DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory:list')
