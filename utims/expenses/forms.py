from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'description', 'receipt']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'receipt': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if not receipt:
            raise forms.ValidationError("A receipt image is required for all expenses.")
        return receipt 