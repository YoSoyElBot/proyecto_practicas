# Generated by Django 5.0.3 on 2024-04-13 02:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_userti_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaTI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreArea', models.CharField(default='Sin nombrar', max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='userti',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.areati'),
        ),
    ]
