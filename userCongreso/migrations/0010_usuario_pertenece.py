# Generated by Django 5.0.3 on 2024-04-08 22:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userCongreso', '0009_remove_area_parent_id_remove_usuario_area_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='pertenece',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userCongreso.area'),
        ),
    ]
