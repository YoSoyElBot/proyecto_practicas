# Generated by Django 5.1.1 on 2024-09-27 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioFEI', '0002_alter_servicio_estado_alter_servicio_fechacierre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='fechaCierre',
            field=models.DateTimeField(blank=True, default='Sin asignar', null=True),
        ),
    ]
