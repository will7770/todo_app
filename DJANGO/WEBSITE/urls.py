from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name = 'logout'),
    path('', views.tasks, name = 'tasks'),
    path('task/<int:pk>', views.TaskUpdate.as_view(), name = 'task'),
    path('task-create/', views.task_create, name = 'task-create'),
    path('task-delete/<int:pk>', views.TaskDelete.as_view(), name = 'task-delete'),
    path('task-reorder/', views.TaskReorder.as_view(), name='task-reorder'),
]