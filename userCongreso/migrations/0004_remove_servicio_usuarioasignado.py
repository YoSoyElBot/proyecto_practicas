# Generated by Django 5.0.3 on 2024-04-03 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userCongreso', '0003_servicio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicio',
            name='usuarioAsignado',
        ),
    ]