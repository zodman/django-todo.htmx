from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

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
    
def todo_edit(request):
    if request.method == "POST":
        todo_name = request.POST.get('todo_name')
        # the `new_todo_name` variable will be None in this case
        # because we didn't send it in the AJAX request
        # we still need it in case the user wants to edit the todo's name
        new_todo_name = request.POST.get('new_todo_name')
        completed = request.POST.get('completed')
        edited_todo = TODO.objects.get(name=todo_name)
        
        # if the `completed` variable is not None this means that the user
        # want to mark the todo as complete/incomplete, otherwise the 
        # user want to edit the todo's name
        if completed:
            if completed == '0':
                edited_todo.completed = False
                edited_todo.save()
                return JsonResponse({'status': 'updated'})
            elif completed == '1':
                edited_todo.completed = True
                edited_todo.save()
                return JsonResponse({'status': 'updated'})

        if TODO.objects.filter(name=new_todo_name).exists():
            return JsonResponse({'status': 'error'})

        edited_todo.name = new_todo_name
        edited_todo.save()
        
        context = {
            'new_todo_name': new_todo_name,
            'status': 'updated'
        }
        return JsonResponse(context)
    
def todo_delete(request):
    if request.method == 'POST':
        todo_name = request.POST.get('todo_name')
        TODO.objects.filter(name=todo_name).delete()
        messages.info(request, "post deleted")
    response = HttpResponse()
    return response
