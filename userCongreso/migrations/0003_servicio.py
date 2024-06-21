# Generated by Django 5.0.3 on 2024-04-03 18:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userCongreso', '0002_rename_areacongreso_area_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('estado', models.CharField(default='abierto', max_length=15)),
                ('fechaCreacion', models.DateTimeField()),
                ('fechaCierre', models.DateTimeField()),
                ('areaSolicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userCongreso.area')),
                ('nombreSolicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userCongreso.usuario')),
                ('responsable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servicios_responsable', to=settings.AUTH_USER_MODEL)),
                ('usuarioAsignado', models.ManyToManyField(blank=True, related_name='servicios_usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
