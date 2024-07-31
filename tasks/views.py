from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task
from django.shortcuts import render, redirect
from .forms import TaskForm
from .serializers import TaskSerializer
import requests

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        response = requests.post('http://127.0.0.1:8000/api/token/', data={
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            data = response.json()
            request.session['access_token'] = data['access']
            return redirect('task-list-view')
        else:
            return render(request, 'login.html', {'error': 'Login failed'})

    return render(request, 'login.html')

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

def task_list_view(request):
    token = request.session.get('access_token', '')
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get('http://127.0.0.1:8000/api/tasks/', headers=headers)
    
    if response.status_code == 200:
        tasks = response.json()
    else:
        tasks = []

    return render(request, 'tasks_list.html', {'tasks': tasks})
