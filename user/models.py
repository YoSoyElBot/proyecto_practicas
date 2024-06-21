from django.db import models
from django.contrib.auth.models import AbstractUser

class AreaTI(models.Model):
    nombreArea = models.CharField(max_length=50, default='Sin nombrar')

    def __str__(self):
        return self.nombreArea


class UserTI(AbstractUser):
    rol = models.CharField(max_length=14,default='No especificado')
    area = models.ForeignKey(AreaTI,on_delete=models.CASCADE)
    cargaTrabajo = models.IntegerField(default=0)
    disponibilidad = models.CharField(max_length=20, default='disponible')
    
