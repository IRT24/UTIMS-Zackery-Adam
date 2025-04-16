from django.db import models

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('SUPPLIES', 'Supplies'),
        ('GROCERIES', 'Groceries'),
        ('UTILITIES', 'Utilities'),
        ('MISC', 'Miscellaneous'),
    ]

    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    receipt = models.ImageField(upload_to='receipts/')

    def __str__(self):
        return f"{self.title} - RM{self.amount}"