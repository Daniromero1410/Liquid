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
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData
import json

@login_required
def home(request):
    """Vista principal del dashboard."""
    context = {
        'user': request.user
    }
    return render(request, 'accounts/home.html', context)

@login_required
def analytics(request):
    """Vista de análisis con estadísticas de usuarios."""
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    recent_users = User.objects.filter(
        date_joined__gte=timezone.now() - timedelta(days=30)
    ).count()

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'recent_users': recent_users
    }
    return render(request, 'accounts/analytics.html', context)

@login_required
def sensor_config(request):
    if request.method == 'POST':
        wifi_config = {
            'ssid': request.POST.get('ssid'),
            'password': request.POST.get('password')
        }
        request.session['wifi_config'] = wifi_config
        return JsonResponse({'status': 'success'})
    
    # Obtener los últimos datos del sensor para mostrar inicialmente
    latest_data = SensorData.objects.all().order_by('-timestamp')[:50]
    context = {
        'latest_data': latest_data
    }
    return render(request, 'accounts/sensor_config.html', context)

@csrf_exempt
def get_sensor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Guardar en la base de datos
            sensor_data = SensorData.objects.create(
                sensor_value=data['sensor_value'],
                humidity_percent=data['humidity_percent']
            )
            return JsonResponse({
                'status': 'success',
                'data': {
                    'timestamp': sensor_data.timestamp.isoformat(),
                    'sensor_value': sensor_data.sensor_value,
                    'humidity_percent': sensor_data.humidity_percent
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # Petición GET - devolver las últimas 50 lecturas
    data = list(SensorData.objects.order_by('-timestamp')[:50].values(
        'timestamp', 'sensor_value', 'humidity_percent'
    ))
    # Invertir para mostrar las más antiguas primero
    data.reverse()
    return JsonResponse(data, safe=False)

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