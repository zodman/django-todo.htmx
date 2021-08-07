
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('todo-list/', views.todo_list, name='todo-list'),
    path('todo-create/', views.todo_create, name='todo-create'),
    path('todo-edit/<int:todo_id>', views.todo_edit, name='todo-edit'),
    path('todo-mark/', views.todo_mark, name='todo-mark'),
    path('todo-delete/', views.todo_delete, name='todo-delete'), # add this
]
