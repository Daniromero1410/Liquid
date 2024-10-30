from django.db import models
from django.contrib.auth.models import User

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sensor_value = models.IntegerField()
    humidity_percent = models.FloatField()

    class Meta:
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"Sensor reading at {self.timestamp}: {self.humidity_percent}%"