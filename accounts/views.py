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
import json
from .models import SensorData
from django.db.models import Avg

# Imports para el modelo de predicción
import numpy as np
import tensorflow as tf
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'core', 'ml_models', 'modelo_resistencia_concreto.h5')
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

# Cargar scaler a partir del dataset de entrenamiento
def get_scaler():
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'core', 'ml_models', 'dataset_concreto_realista_ajustado.csv')
    data = pd.read_csv(dataset_path)
    X = data.drop(['resistencia_psi', 'resistencia_mpa'], axis=1)
    scaler = StandardScaler()
    scaler.fit(X)
    return scaler

scaler = get_scaler()

# ============================================
# VISTAS
# ============================================

@login_required
def home(request):
     # Total de usuarios activos
    total_active_users = User.objects.filter(is_active=True).count()

    # Total de lecturas de sensores
    total_readings = SensorData.objects.count()

    # Última resistencia predicha (dummy por ahora si quieres)
    ultima_prediccion_resistencia = SensorData.objects.aggregate(
        promedio_humedad=Avg('humidity_percent')
    )['promedio_humedad']

    # Si no hay lecturas, ponemos 0
    if ultima_prediccion_resistencia is None:
        ultima_prediccion_resistencia = 0

    context = {
        'total_active_users': total_active_users,
        'total_readings': total_readings,
        'ultima_prediccion_resistencia': round(ultima_prediccion_resistencia, 2),
        'user': request.user
    }
    return render(request, 'accounts/home.html', context)

@login_required
def sensor_config(request):
    return render(request, 'accounts/sensor_config.html')

@login_required
@csrf_exempt
def analytics(request):
    total_readings = SensorData.objects.count()
    recent_readings = SensorData.objects.filter(
        timestamp__gte=timezone.now() - timedelta(hours=24)
    ).count()

    prediction_result = None
    input_data = {}

    if request.method == 'POST':
        try:
            cemento = float(request.POST.get('cemento_kgm3'))
            arena = float(request.POST.get('arena_m3'))
            grava = float(request.POST.get('grava_m3'))
            humedad = float(request.POST.get('humedad_sensor'))

            input_data = {
                'cemento': cemento,
                'arena': arena,
                'grava': grava,
                'humedad': humedad,
            }

            # Calcular automáticamente relación agua/cemento
            def calcular_relacion_agua_cemento(humedad_sensor):
                w_c_min = 0.35
                w_c_max = 0.75
                humedad_normalizada = 1 - (humedad_sensor / 1023)
                relacion = w_c_min + (w_c_max - w_c_min) * humedad_normalizada
                return round(relacion, 3)

            relacion = calcular_relacion_agua_cemento(humedad)

            # Preparar entrada para el modelo
            features = np.array([[cemento, arena, grava, relacion, humedad]])
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0][0]

            prediction_result = round(prediction, 2)

        except Exception as e:
            prediction_result = f"Error: {str(e)}"

    context = {
        'total_readings': total_readings,
        'recent_readings': recent_readings,
        'prediction_result': prediction_result,
        'input_data': input_data,
    }
    return render(request, 'accounts/analytics.html', context)

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_value = data.get('sensor_value')
            humidity_percent = data.get('humidity_percent')

            if sensor_value is None or humidity_percent is None:
                return JsonResponse({'status': 'error', 'message': 'Missing required data'}, status=400)

            SensorData.objects.create(
                sensor_value=sensor_value,
                humidity_percent=humidity_percent
            )

            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@login_required
def view_data(request):
    try:
        data = SensorData.objects.all()[:50]
        data_list = [{
            'timestamp': reading.timestamp.isoformat(),
            'sensor_value': reading.sensor_value,
            'humidity_percent': reading.humidity_percent
        } for reading in data]
        return JsonResponse({"data": data_list})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# CRUD de Usuarios

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
