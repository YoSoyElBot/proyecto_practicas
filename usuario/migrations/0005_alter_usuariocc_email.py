# Generated by Django 5.1.1 on 2024-10-11 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0004_alter_rol_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariocc',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
