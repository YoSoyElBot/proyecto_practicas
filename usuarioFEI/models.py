from django.db import models
from django.db import models
from usuario.models import usuarioCC
from django.db import models

class Problemas(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre  # Asegúrate de que el nombre se muestre correctamente

class Area(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre  # Este método ya está bien

class Servicio(models.Model):
    ESTADOS = [
        ('solicitado', 'Solicitado'),
        ('asignado', 'Asignado'),
        ('en_atencion', 'En Atención'),
        ('finalizado', 'Finalizado'),
    ]
    
    folio = models.CharField(max_length=20, unique=True, blank=True)  # Permitir que esté vacío al crear
    nombreSolicitante = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300)
    responsable = models.ForeignKey(usuarioCC, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios_responsable')
    problema = models.ForeignKey(Problemas, on_delete=models.CASCADE, null=True)
    areaSolicitante = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='solicitado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaCierre = models.DateTimeField(null=True, blank=True)
    comentarios = models.TextField(max_length=350, default='sin comentar')

    def __str__(self):
        return f'{self.nombreSolicitante} - {self.problema.nombre} - {self.responsable} '   # Combina la información

    def save(self, *args, **kwargs):
        if not self.folio:  # Si el folio no ha sido asignado aún
            last_service = Servicio.objects.order_by('id').last()
            if last_service and last_service.folio:
                last_folio = last_service.folio
                new_folio = str(int(last_folio) + 1).zfill(5)  # Incrementa y rellena con ceros
            else:
                new_folio = '001'  # Folio inicial

            self.folio = new_folio  # Asignamos el nuevo folio
        super().save(*args, **kwargs)