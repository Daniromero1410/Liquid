from django.db import models
from django.contrib.auth.models import User

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sensor_value = models.IntegerField()
    humidity_percent = models.FloatField()

    class Meta:
        ordering = ['-timestamp']

class WifiConfig(models.Model):
    ssid = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'