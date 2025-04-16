from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Expense  # Ensure you have this model
from .forms import ExpenseForm

class ExpenseListView(ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get sort parameters
        sort_by = self.request.GET.get('sort', 'date')  # Default sort by date
        order = self.request.GET.get('order', 'desc')   # Default descending order
        
        # Define valid sort fields and their corresponding model fields
        valid_sort_fields = {
            'category': 'category',
            'amount': 'amount',
            'date': 'date'
        }
        
        # Apply sorting if valid field
        if sort_by in valid_sort_fields:
            order_field = valid_sort_fields[sort_by]
            if order == 'desc':
                order_field = f'-{order_field}'
            queryset = queryset.order_by(order_field)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'date')
        context['current_order'] = self.request.GET.get('order', 'desc')
        return context

class ExpenseCreateView(CreateView):
    model = Expense
    template_name = 'expenses/expense_form.html'
    form_class = ExpenseForm
    
    def get_success_url(self):
        return reverse_lazy('expenses:detail', kwargs={'pk': self.object.pk})

class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'
    context_object_name = 'expense'

class ExpenseUpdateView(UpdateView):
    model = Expense
    template_name = 'expenses/expense_form.html'
    form_class = ExpenseForm
    
    def get_success_url(self):
        return reverse_lazy('expenses:detail', kwargs={'pk': self.object.pk})

class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:list')