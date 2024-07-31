from django.urls import path
from .views import TaskListCreateView, TaskDetailView, task_list_view, login_view

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),  # Endpoint untuk list dan create
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),  # Endpoint untuk detail task
    path('tasks/list/', task_list_view, name='task-list-view'),  # URL untuk tampilan daftar tugas
    path('login/', login_view, name='login'),  # URL untuk login
]
