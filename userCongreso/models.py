from django.db import models
from user.models import UserTI
# Create your models here.

from django.db import models

class Area(models.Model):
    nombre = models.CharField(max_length=150) # Este campo indica el usuario responsable de esta área
    def __str__(self):
        return self.nombre
    
class Problema(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    pertenece = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    serviciosSolicitados = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    folio = models.CharField(max_length=20, unique=True, default=000000)
    nombreSolicitante = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300)
    responsable = models.ForeignKey(UserTI, on_delete=models.SET_NULL, null=True, related_name='servicios_responsable')
    problema = models.ForeignKey(Problema, on_delete=models.CASCADE,null=True)
    areaSolicitante = models.ForeignKey(Area, on_delete=models.CASCADE)
    estado = models.CharField(max_length=15, default='abierto')
    fechaCreacion = models.DateTimeField()
    comentarios = models.TextField(max_length=350,default='sin comentar')
    fechaCierre = models.DateTimeField(null=True)
    

