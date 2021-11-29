from django.urls import path

from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomLoginView,RegisterPage
from django.contrib.auth.views import LogoutView

# directly class can't be used in views so as_view() is used
urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'), #once logged out which page user should be send to next
    path('register/',RegisterPage.as_view(),name='register'),
    path('',TaskList.as_view(),name='tasks'),
    
    # will look for key for each task
    path('task/<int:pk>/', TaskDetail.as_view(),name='task'),
    path('task-create/', TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(),name='task-delete'),
]