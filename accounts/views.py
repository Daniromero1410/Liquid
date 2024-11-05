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
from django.db import connections
import json

@login_required
def home(request):
    """Vista principal del dashboard."""
    context = {
        'user': request.user
    }
    return render(request, 'accounts/home.html', context)

@login_required
def sensor_config(request):
    """Vista de configuración del sensor."""
    return render(request, 'accounts/sensor_config.html')

@login_required
def analytics(request):
    """Vista de análisis con estadísticas."""
    total_readings = 0
    recent_readings = 0
    
    try:
        with connections['conexion'].cursor() as cursor:
            # Get total readings
            cursor.execute("SELECT COUNT(*) FROM lectura_higrometro")
            total_readings = cursor.fetchone()[0]
            
            # Get recent readings (last 24 hours)
            cursor.execute("""
                SELECT COUNT(*) FROM lectura_higrometro 
                WHERE fecha_lectura >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
            """)
            recent_readings = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error getting analytics: {e}")

    context = {
        'total_readings': total_readings,
        'recent_readings': recent_readings,
    }
    return render(request, 'accounts/analytics.html', context)

@csrf_exempt
def sensor_data_api(request):
    """API para obtener datos del sensor desde MySQL."""
    if request.method == 'GET':
        try:
            with connections['conexion'].cursor() as cursor:
                cursor.execute("""
                    SELECT id, valor_sensor, porcentaje_humedad, fecha_lectura 
                    FROM lectura_higrometro 
                    ORDER BY fecha_lectura DESC 
                    LIMIT 50
                """)
                columns = [col[0] for col in cursor.description]
                data = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
                
                # Format data for frontend
                formatted_data = [{
                    'id': row['id'],
                    'sensor_value': row['valor_sensor'],
                    'humidity_percent': row['porcentaje_humedad'],
                    'timestamp': row['fecha_lectura'].isoformat() if row['fecha_lectura'] else None
                } for row in data]
                
                return JsonResponse(formatted_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# User management views
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