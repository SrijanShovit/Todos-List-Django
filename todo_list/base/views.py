from django.shortcuts import render,redirect
# from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import  LoginView
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy
from .models import Task

# in function based view we would have to do all task from own but using class based view
# django does it all by itself


# Create your views here.
# function based view
# def taskList(request):
#     return HttpResponse('To do list')

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True #prevent user from being on this page once they r logged in
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()  #once form is valid and saved user is return
        if user is not None:
            login(self.request,user)  #redirect user to home page on sign up only(login functionhandles this)
        return super(RegisterPage, self).form_valid(form)
    
    #restricting logged in user from logging and regitering
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args,**kwargs)

# this looked for task_list.html
#now this view is restricted 
class TaskList(LoginRequiredMixin,ListView): 
    model = Task
    context_object_name = 'tasks'
    
    #user should get their own data not others'
    def get_context_data(self,**kwargs):
        #way of passing extra data
        context = super().get_context_data(**kwargs)
        #filtering tasks only of current user
        context['tasks'] =  context['tasks'].filter(user=self.request.user)
        #getting count of incomplete tasks
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input
            )
            
        context['search-input'] = search_input
        return context
    
    
#this will look for task_detail.html
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'  #look for task.html and not task_detail.html
    
    
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'complete'] 
    success_url = reverse_lazy('tasks')  #if everything goes correct redirect user to given view
    
    # overriding to set current user as default creator of task in their account
    def form_valid(self, form):
        form.instance.user = self.request.user
        #after that proceed with normal working
        return super(TaskCreate,self).form_valid(form)

    
    
# this will also look for task_form.html
class TaskUpdate(LoginRequiredMixin,UpdateView):
    
    model = Task
    #fields = '__all__'  #it 'll create form by default for us with all fields specified as per model given
    fields = ['title', 'description', 'complete'] 
    success_url = reverse_lazy('tasks')
    
#looks for task_confirm_delete.html
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    fields = '__all__' 
    success_url = reverse_lazy('tasks')
    
    