from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
#from bd.models import UsuarioTI, Area
from django import forms
from user.models import UserTI, AreaTI
from userCongreso.models import Area, Usuario, Servicio, Problema
from django.forms import ModelForm, CharField, ChoiceField, ModelChoiceField


class FormUserTICreationForm(forms.ModelForm):
    ROLES_CHOICES = [
        ('tecnico', 'Técnico'),
        ('administrador', 'Administrador'),
        ('supervisor' , 'Supervisor'),
    ]


    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices=ROLES_CHOICES)
    area = forms.ModelChoiceField(queryset=AreaTI.objects.all(), empty_label="Seleccione un área")

    class Meta:
        model = UserTI  # Especifica el modelo asociado
        fields = ['first_name', 'last_name', 'password', 'rol', 'area']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nombre de usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=128, label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ServicioForm(forms.Form):
    nombreSolicitante = forms.CharField(max_length=100) 
    descripcion = forms.CharField(max_length=100)
    areaSolicitante = forms.ModelChoiceField(queryset=Area.objects.all(), label="Área Solicitante:")
    problema = forms.ModelChoiceField(queryset=Problema.objects.all(), label="Catálogo de problemas: ")
    
class ProblemaForm(forms.Form):
    nombre = forms.CharField(max_length=25)

class AltaAreaForm(forms.Form):
   area = forms.CharField(max_length=150)

class UsuarioCongresoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'pertenece']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget = forms.TextInput(attrs={'placeholder': 'Nombre del usuario'})
        self.fields['pertenece'].queryset = Area.objects.all()  # Establecer queryset para el campo pertenece

class CerrarServicioForm(forms.Form):
    ACCIONES_CHOICES = (
        ('cerrar', 'Cerrar'),
        ('posponer', 'Posponer'),
    )
    
    accion = forms.ChoiceField(choices=ACCIONES_CHOICES, label='Acción a realizar')
    comentarios = forms.CharField(widget=forms.Textarea, label='Comentarios')


class CambioContraseñaForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=UserTI.objects.all(), label='Usuario')
    nueva_contraseña = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

 















 
#class ServicioForm(forms.ModelForm):
#    class Meta:
#        model = Servicios
#        fields = ['solicitadoPor', 'areaSolicitante', 'descripción', 'asignado', 'estado', 'tipo']

#    GeneradoPor = forms.CharField(max_length=50, required=True, label='Escriba su nombre')
#    areaAtendida = forms.ModelChoiceField(queryset=Areas.objects.all(), label='Selecciona el area del problema:', required=True, empty_label='Selecciona una area:')
#    tipo = forms.ChoiceField(choices=Servicios._meta.get_field('tipo').choices, label='Tipo de problema', required=True)
