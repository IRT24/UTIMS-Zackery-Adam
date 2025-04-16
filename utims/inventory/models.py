from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    low_stock_threshold = models.PositiveIntegerField(default=5)  # Alert threshold
    last_updated = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    def __str__(self):
        return f"{self.name} - {self.quantity} units"

class InventoryLog(models.Model):
    ACTIONS = [
        ('ADD', 'Added'),
        ('REMOVE', 'Removed'),
        ('UPDATE', 'Updated'),
    ]
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTIONS)
    quantity_changed = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.item.name} - {self.action} {self.quantity_changed} units"