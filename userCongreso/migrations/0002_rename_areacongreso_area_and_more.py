# Generated by Django 5.0.3 on 2024-04-03 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userCongreso', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AreaCongreso',
            new_name='Area',
        ),
        migrations.RenameModel(
            old_name='UsuarioCongreso',
            new_name='Usuario',
        ),
    ]