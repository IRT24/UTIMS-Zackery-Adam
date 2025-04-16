from django import forms
from .models import Task
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assignee']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].queryset = User.objects.filter(role='employee', is_active=True)
        self.fields['assignee'].required = False
        self.fields['assignee'].label = "Assign to employee"
    
    def auto_assign(self):
        """Automatically assign the task to a random active employee"""
        employees = User.objects.filter(role='employee', is_active=True)
        if employees.exists():
            # Choose a random employee
            random_employee = random.choice(employees)
            self.instance.assignee = random_employee
            return True
        return False 