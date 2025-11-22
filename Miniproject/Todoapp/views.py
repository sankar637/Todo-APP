from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task
from .forms import TaskForm

def home(request):
    tasks = Task.objects.all().order_by('-id')

    # Check overdue tasks & mark notified
    alerts = []
    now = timezone.now()

    for task in tasks:
        if task.due_datetime and task.due_datetime <= now and not task.notified:
            alerts.append(f'Task "{task.title}" time is completed!')
            task.notified = True
            task.save()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm()

    context = {
        'tasks': tasks,
        'form': form,
        'alerts': alerts,
    }
    return render(request, 'todo/home.html', context)

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('home')

def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('home')
