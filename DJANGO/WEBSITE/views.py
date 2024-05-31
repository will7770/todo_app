from django.shortcuts import render, redirect
from .forms import RegisterUser, LoginUser, AddTask, PositionForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db import transaction



def register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            login(request, user)
            messages.success(request, "You have been registered.")
            return redirect('tasks')
    else:
        form = RegisterUser()
        
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def log_in(request):
    if request.method == 'POST':
        form = LoginUser(request.POST)
        #if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('tasks')
        else:
            messages.error(request, "There might be an error in your username or password, make sure its right and exists.")
            return redirect('login')
    #else:
            messages.error(request, "2 There Was An Error Logging In, Please Try Again...")
    else:
        form = LoginUser()

    context = {'form': form}
    return render(request, 'registration/login.html', context)


def log_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('tasks')


def tasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.all()
        user_tasks = tasks.filter(user=request.user)
        return render(request, 'home2.html', context={'tasks': user_tasks})
    else:
        #messages.success(request, message="You can't view that page")
        return redirect('login')

    
@login_required(login_url='login/')    
def task_create(request):
    if request.method == 'POST':
        form = AddTask(request.POST)
        task = form.save()
        task.user = request.user
        task.save()
        messages.success(request, message='Successfully added a new task!')
        return redirect('tasks')
    else:
        form = AddTask()
    context = {'form': form}
    return render(request, 'task-create.html', context=context)

class TaskDelete(DeleteView, LoginRequiredMixin):
    model = Task
    success_url = reverse_lazy('tasks')
    login_url = 'login/'
    template_name = 'task-delete.html'



class TaskUpdate(UpdateView, LoginRequiredMixin):
    model = Task
    fields = ['title', 'description', 'status']
    success_url = reverse_lazy('tasks')
    login_url = 'login/'
    template_name = 'task.html'


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
    

# --- FUNCTION BASED VIEW FOR UPDATING A TASK

# def task_update(request, pk):
#     if request.method == 'POST':
#         specific_task = Task.objects.get(id=pk)
#         form = UpdateTask(request.POST, instance=specific_task)
#         task = form.save()
#         task.save()
#         messages.success(request, message='Successfully changed a task!')
#         return redirect('tasks')
#     else:
#         form = UpdateTask()
#     context = {'form': form}
#     return render(request, 'task-update.html', context=context)