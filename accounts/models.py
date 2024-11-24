from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sensor_value = models.IntegerField()
    humidity_percent = models.FloatField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.timestamp} - {self.humidity_percent}%'