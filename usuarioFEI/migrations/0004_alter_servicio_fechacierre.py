# Generated by Django 5.1.1 on 2024-09-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioFEI', '0003_alter_servicio_fechacierre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='fechaCierre',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
