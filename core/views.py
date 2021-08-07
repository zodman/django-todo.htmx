from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods


from django.urls import reverse

from .models import TODO


def home(request):
    return render(request, 'todo.html')

def todo_list(request):
    todos = TODO.objects.all()
    context = {'todos': list(todos.values())}
    return render(request, "_todo_list.html", context)

def todo_create(request):
    if request.method == 'POST':
        todo_name = request.POST.get('todo_name')
        todo = TODO.objects.filter(name=todo_name)

        # we need to make sure that this todo does not exist in the database
        if todo.exists():
            messages.error(request, "todo exists")
        else:
            messages.info(request, "todo added")
            TODO.objects.create(name=todo_name)
    response = HttpResponse("")
    response["HX-Redirect"]=reverse("home")
    response["HX-Refresh"]=True
    return response
 
@require_http_methods(["POST",])
def todo_mark(request):
    todo_name = request.POST.get('todo_name')
    completed = request.POST.get('completed')
    edited_todo = TODO.objects.get(name=todo_name)
    if completed:
        if completed == '0':
            edited_todo.completed = False
            edited_todo.save()
        elif completed == '1':
            edited_todo.completed = True
            edited_todo.save()
    resp = HttpResponse()
    resp["HX-Refresh"]=True
    resp["HX-Redirect"]=reverse("home")
    return  resp

@require_http_methods(["POST","GET"])
def todo_edit(request, todo_id=None):
    todo = TODO.objects.get(id=todo_id)
    if request.method== "GET":
        context = {
            'todo': todo
        }
        return render(request, "_edit_form.html", context)
    else:
        new_todo_name = request.POST.get("new_todo_name")
        todo.name = new_todo_name
        todo.save()
    response = HttpResponse()
    response["HX-Redirect"]=reverse("home")
    response["HX-Refresh"]=True
    return response
    
def todo_delete(request):
    if request.method == 'POST':
        todo_name = request.POST.get('todo_name')
        TODO.objects.filter(name=todo_name).delete()
        messages.info(request, "post deleted")
    response = HttpResponse()
    return response
