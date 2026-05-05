from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm

@login_required
def dashboard(request):
    projects = Project.objects.filter(created_by=request.user)
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/dashboard.html', {'projects': projects, 'tasks': tasks})

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tasks/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'tasks/project_form.html', {'form': form})

@login_required
def task_list(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project)
    return render(request, 'tasks/task_list.html', {'project': project, 'tasks': tasks})

@login_required
def task_create(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('task_list', pk=pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'project': project})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list', pk=task.project.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'project': task.project})