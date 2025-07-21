from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task


def index(request):
    if request.method == 'POST':
        title = request.POST['title']
        due_at_raw = request.POST['due_at']
        priority_raw = request.POST.get('priority', 1)  # priority欄がなければ1に

        if due_at_raw:
            due_at = make_aware(parse_datetime(due_at_raw))
        else:
            due_at = None

        try:
            priority = int(priority_raw)
        except ValueError:
            priority = 1

        task = Task(title=title, priority=priority, due_at=due_at)
        task = Task(title=request.POST['title'], comment=request.POST.get('comment', ''),
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()
        return redirect('index')

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    elif request.GET.get('order') == 'comp':
        tasks = Task.objects.order_by('completed')
    else:
        tasks = Task.objects.order_by('-posted_at')
        
    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')

    context = {
            'task': task
        }
    return render(request, 'todo/detail.html', context)

def close(request, task_id):
    try:
        task = Task.objects.get(pk = task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)
  
def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    task.delete()
    return redirect(index)
  
def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.comment = request.POST.get('comment', '')
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail, task_id)
    
    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)


def priority(request, task_id):
    if request.method == 'POST':
        task = Task(title=request.POST['priority'],
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('priority')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)
