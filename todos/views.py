from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Todo
from .forms import TodoForm


class TodoListView(ListView):
    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        queryset = Todo.objects.all()
        # Filter by status tab
        status = self.request.GET.get('status', 'all')
        if status == 'active':
            queryset = queryset.filter(completed=False)
        elif status == 'completed':
            queryset = queryset.filter(completed=True)
        # Search
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        # Filter by priority
        priority = self.request.GET.get('priority', '')
        if priority in ['low', 'medium', 'high']:
            queryset = queryset.filter(priority=priority)
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_todos = Todo.objects.all()
        ctx['total'] = all_todos.count()
        ctx['completed_count'] = all_todos.filter(completed=True).count()
        ctx['pending_count'] = all_todos.filter(completed=False).count()
        ctx['status'] = self.request.GET.get('status', 'all')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['priority_filter'] = self.request.GET.get('priority', '')
        ctx['completion_pct'] = (
            int((ctx['completed_count'] / ctx['total']) * 100)
            if ctx['total'] > 0 else 0
        )
        return ctx


class TodoCreateView(CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Create New Task'
        ctx['submit_label'] = 'Create Task'
        return ctx


class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Edit Task'
        ctx['submit_label'] = 'Save Changes'
        return ctx


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')


def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')