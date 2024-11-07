from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django import forms
from usuario.models import usuarioCC
from usuarioFEI.models import Area, Servicio, Problemas
from django.forms import ModelForm, CharField, ChoiceField, ModelChoiceField


from django import forms
from usuario.models import usuarioCC, Rol

class FormUsuarioCC(forms.ModelForm):
    class Meta:
        model = usuarioCC
        fields = ['first_name', 'last_name', 'rol', 'email']  # Quitar 'area' del formulario


    def __init__(self, *args, **kwargs):
        super(FormUsuarioCC, self).__init__(*args, **kwargs)
        # Obtener los roles desde la base de datos y agregarlos al campo de selección
        self.fields['rol'].queryset = Rol.objects.all()

class BajaUsuarioForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=usuarioCC.objects.all(), label="Seleccione el usuario", empty_label="Seleccione un usuario")
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nombre de usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=128, label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    
class LoginForm2(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class LoginForm3(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')


class ServicioForm(forms.Form):
    nombreSolicitante = forms.CharField(max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea, max_length=500)
    areaSolicitante = forms.ModelChoiceField(queryset=Area.objects.all(), label="Área solicitante")
    problema = forms.ModelChoiceField(queryset=Problemas.objects.all(), label="Catálogo de problemas")

class ServicioFormExtra(forms.Form):
    descripcion = forms.CharField(widget=forms.Textarea, max_length=500)
    areaSolicitante = forms.ModelChoiceField(queryset=Area.objects.all(), label="Área solicitante")
    problema = forms.ModelChoiceField(queryset=Problemas.objects.all(), label="Catálogo de problemas")
    
class ProblemaForm(forms.Form):
    nombre = forms.CharField(max_length=25)

class BajaProblemaForm(forms.Form):
    problema = forms.ModelChoiceField(queryset=Problemas.objects.all(),empty_label='Selecciona el problema:')

class AltaAreaForm(forms.Form):
   area = forms.CharField(max_length=50)

class BajaAreaForm(forms.Form):
    area = forms.ModelChoiceField(queryset=Area.objects.all(), empty_label='Selecciona el area:')

class CerrarServicioForm(forms.Form):
    ACCIONES_CHOICES = (
        ('cerrar', 'Cerrar'),
        ('posponer', 'Posponer'),
    )
    
    accion = forms.ChoiceField(choices=ACCIONES_CHOICES, label='Acción a realizar')
    comentarios = forms.CharField(widget=forms.Textarea, label='Comentarios')


class CambioContraseñaForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=usuarioCC.objects.all(), label='Usuario')
    nueva_contraseña = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
