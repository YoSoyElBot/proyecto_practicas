# Generated by Django 5.0.3 on 2024-06-21 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userCongreso', '0020_alter_problema_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='fechaCierre',
            field=models.DateTimeField(default='sin asignar', null=True),
        ),
    ]