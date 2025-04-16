from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Task  # Ensure Task model exists
from .forms import TaskForm

class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"  # Ensure this template exists in templates/tasks/
    context_object_name = "tasks"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get sort parameters
        sort_by = self.request.GET.get('sort', 'due_date')  # Default sort by due date
        order = self.request.GET.get('order', 'asc')    # Default ascending order
        
        # Define valid sort fields and their corresponding model fields
        valid_sort_fields = {
            'status': 'status',
            'priority': 'priority',
            'due_date': 'due_date'
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
        context['current_sort'] = self.request.GET.get('sort', 'due_date')
        context['current_order'] = self.request.GET.get('order', 'asc')
        return context

class TaskCreateView(CreateView):
    model = Task
    template_name = "tasks/task_form.html"
    form_class = TaskForm
    success_url = reverse_lazy('tasks:list')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        auto_assign = 'auto_assign' in request.POST
        
        if form.is_valid():
            if auto_assign:
                if form.auto_assign():
                    messages.success(request, "Task has been automatically assigned to an employee.")
                else:
                    messages.error(request, "No active employees found to assign this task to.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class TaskUpdateView(UpdateView):
    model = Task
    template_name = "tasks/task_form.html"
    form_class = TaskForm
    success_url = reverse_lazy('tasks:list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        auto_assign = 'auto_assign' in request.POST
        
        if form.is_valid():
            if auto_assign:
                if form.auto_assign():
                    messages.success(request, "Task has been automatically assigned to an employee.")
                else:
                    messages.error(request, "No active employees found to assign this task to.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy('tasks:list')
