from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import SensorData
import json


class UserListView(ListView):
    model = User 
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'is_active', 'is_staff']
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

@login_required
def home(request):
    return render(request, 'accounts/home.html')

@login_required
def analytics(request):
   
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'recent_users': recent_users,
    }
    return render(request, 'accounts/analytics.html', context)

@login_required
def sensor_config(request):
    if request.method == 'POST':
        # Guardar configuración WiFi
        wifi_config = {
            'ssid': request.POST.get('ssid'),
            'password': request.POST.get('password')
        }
        # Aquí deberías implementar la lógica para guardar la configuración
        # y enviarla al dispositivo ESP32
        return JsonResponse({'status': 'success'})
    return render(request, 'accounts/sensor_config.html')

@login_required
def get_sensor_data(request):
    # Obtener los últimos 50 registros
    data = SensorData.objects.order_by('-timestamp')[:50]
    sensor_data = [{
        'timestamp': entry.timestamp,
        'sensor_value': entry.sensor_value,
        'humidity_percent': entry.humidity_percent
    } for entry in data]
    return JsonResponse(sensor_data, safe=False)