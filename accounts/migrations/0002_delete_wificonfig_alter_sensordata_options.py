# Generated by Django 5.1.2 on 2024-11-04 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WifiConfig',
        ),
        migrations.AlterModelOptions(
            name='sensordata',
            options={'get_latest_by': 'timestamp', 'ordering': ['-timestamp']},
        ),
    ]
