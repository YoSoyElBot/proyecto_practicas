from system import settings
import secrets
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from user.models import UserTI, AreaTI
from userCongreso.models import Area, Servicio, Usuario, Problema
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from system.forms import FormUserTICreationForm, LoginForm, AltaAreaForm, UsuarioCongresoForm, ServicioForm, ProblemaForm, CambioContraseñaForm
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.views.decorators.csrf import requires_csrf_token




##################### VISTAS DE FUNCIONALIDADES ###############################################333
def rol_requerido(rol):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not request.user.is_authenticated:
                return redirect('login')  # Redireccionar a la página de inicio de sesión si el usuario no ha iniciado sesión

            # Verificar si el usuario tiene el rol adecuado
            if request.user.rol != rol:
                # Puedes personalizar este mensaje de error según tus necesidades
                return redirect('error')  # Cambia 'pagina_de_inicio' por la URL de tu página de inicio

            # Si el usuario está autenticado y tiene el rol adecuado, ejecutar la vista original
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

######################## VISTA PARA MATAR LA COOKIE DE SESION DE LOS USUARIOS ##########################
def cerrar_sesion(request):
    logout(request)  
    return redirect('/login/')

############# VISTA PARA MOSTRAR LOS ERRORES DE USUARIO ###########
def errores(request):
    return render(request, 'errores.html')

########################## VISTA PARA LOGUEARSE AL SISTEMA DEPENDIENDO DE SU ROL, ESTA FUNCION UTILIZADA 
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redireccionar según el rol del usuario
                if user.rol == 'tecnico':
                    return redirect('tec_index')  # Cambia 'tec_index' por la URL del técnico
                elif user.rol == 'administrador':
                    return redirect('admin_index')  # Cambia 'admin_index' por la URL del administrador
                elif user.rol == 'supervisor':
                    return redirect('supervisor_index')
                else:
                    # Rol no reconocido, muestra un mensaje de error
                    messages.error(request, 'Rol de usuario no reconocido.')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

############## VISTA PARA TRATAR LOS ERRORES CSRF ########################3


def csrf_error_view(request):
    # Aquí puedes renderizar una página de error CSRF personalizada
    return render(request, 'csrf.html')



########################## VISTAS DE TECNICO ##################################
@rol_requerido('tecnico')
@login_required(login_url='login')
def tec_index(request):
    return render(request, 'tec_index.html')

from django.shortcuts import render

@rol_requerido('tecnico')
@login_required(login_url='login')
def dashboard_tecnico(request):
    # Obtener el usuario actualmente autenticado
    usuario_actual = request.user

    # Obtener los servicios asignados al usuario actual
    servicios_asignados = Servicio.objects.filter(responsable=usuario_actual)

    # Renderizar la plantilla del dashboard y pasar los servicios asignados como contexto
    return render(request, 'dashboard.html', {'servicios_asignados': servicios_asignados})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CerrarServicioForm


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@rol_requerido('tecnico')
@login_required(login_url='login')
def servicios_abiertos(request):
    # Obtener los servicios asignados al usuario actual que estén en estado "abierto"
    servicios_abiertos = Servicio.objects.filter(responsable=request.user, estado='abierto')

    # Pasar los servicios asignados como contexto al template 'servicios_abiertos.html'
    return render(request, 'servicios_abiertos.html', {'servicios_abiertos': servicios_abiertos})

@rol_requerido('tecnico')
@login_required(login_url='login')
def cerrar_servicio(request):
    if request.method == 'POST':
        servicio_id = request.POST.get('servicio_id')
        servicio = Servicio.objects.get(pk=servicio_id, responsable=request.user, estado='abierto')
        comentario = request.POST.get('comentario')
        servicio.comentarios = comentario
        servicio.estado = 'cerrado'
        servicio.fechaCierre = timezone.now()  # Agregar la fecha de cierre
        servicio.save()
        messages.success(request, 'El servicio se ha cerrado correctamente.')

    # Obtener los servicios asignados al usuario actual que estén en estado "abierto"
    servicios_abiertos = Servicio.objects.filter(responsable=request.user, estado='abierto')

    # Pasar los servicios asignados como contexto al template 'cerrar.html'
    return render(request, 'cerrar.html', {'servicios_abiertos': servicios_abiertos})





######################## VISTAS DE SUPERVISOR ###################################
def servicios_abiertos(request):
    # Obtener todos los servicios con estado 'abierto'
    servicios_abiertos = Servicio.objects.filter(estado='abierto')

    # Pasar los servicios abiertos como contexto al template
    return render(request, 'servicios_abiertos.html', {'servicios_abiertos': servicios_abiertos})


def servicios_cerrados(request):
    # Obtener todos los servicios con estado 'cerrado'
    servicios_cerrados = Servicio.objects.filter(estado='cerrado')

    # Pasar los servicios cerrados como contexto al template
    return render(request, 'servicios_cerrados.html', {'servicios_cerrados': servicios_cerrados})


@rol_requerido('supervisor')
@login_required(login_url='login')
def supervisor_index(request):
    return render(request, 'supervisor_index.html')

@rol_requerido('supervisor')
@login_required(login_url='login')
def ver_tecnicos(request):
    # Obtener todos los usuarios técnicos
    tecnicos = UserTI.objects.all()

    # Pasar los usuarios técnicos como contexto al template 'ver_tecnicos.html'
    return render(request, 'tecnicos.html', {'tecnicos': tecnicos})



######################## VISTAS DE ADMINISTRADOR #######################################################
######################### VISTA PARA MOSTRAR EL INDEX DEL ADMINISTRADOR #####################333
@rol_requerido('administrador')
@login_required(login_url='login')
def admin_index(request):
    return render(request, 'admin_index.html')

############################ VISTA PARA DAR DE ALTA A UN AREA DEL  ############################3333
@requires_csrf_token
@rol_requerido('tecnico')
@login_required(login_url='login')
def dashboard_tecnico(request):
    # Obtener el usuario actualmente autenticado
    usuario_actual = request.user

    # Obtener los servicios asignados al usuario actual
    servicios_asignados = Servicio.objects.filter(responsable=usuario_actual)

    # Renderizar la plantilla del dashboard y pasar los servicios asignados como contexto
    return render(request, 'dashboard.html', {'servicios_asignados': servicios_asignados})


def alta_area(request):
    if request.method == 'POST':
        form = AltaAreaForm(request.POST)
        if form.is_valid():
            nombre_area = form.cleaned_data['area']
            area = Area(nombre=nombre_area)
            area.save()  # Guardamos la instancia del modelo
            messages.success(request, 'Área creada exitosamente!')
        else:
            messages.error(request, 'No se ha podido crear el área')
    else:
        form = AltaAreaForm()
    return render(request, 'altaarea.html', {'form': form})
################ VISTA PARA DAR DE ALTA PROBLEMAS ###########################
@rol_requerido('administrador')
@login_required(login_url='login')
def alta_problemas(request):
    if request.method == 'POST':
        form = ProblemaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            nombre = Problema(nombre=nombre)
            nombre.save()
            messages.success(request,'El problema se ha agregado exitosamente!')
        else:
            messages.error(request, 'No se ha podido agregar el problema')
    else:
        form= ProblemaForm()
    return render(request, 'altaproblemas.html', {'form': form})



######################### VISTA PARA DAR DEL ALTA UN USUARIO GENRICO NO TI DEL CONGRESO #############333
@rol_requerido('administrador')
@login_required(login_url='login')
def agregar_usuario(request):
    areas = Area.objects.all()  # Obtener todas las áreas para el contexto
    if request.method == 'POST':
        form = UsuarioCongresoForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            
            # Verificar si se seleccionó un área
            if usuario.pertenece:
                usuario.save()
                messages.success(request, 'Usuario creado exitosamente!')
              # Redirigir a la página de éxito
            else:
                messages.error(request, 'Debes seleccionar un área.')
        else:
            messages.error(request, 'Hubo un error al crear el usuario. Por favor, revisa los datos ingresados.')
    else:
        form = UsuarioCongresoForm()
    
    return render(request, 'altauser.html', {'form': form, 'areas': areas})



##################### VISTA PARA AGREGAR UN NUEVO USUARIO DE TI #################################3333
@rol_requerido('administrador')
@login_required(login_url='login')
def crear_usuario_ti(request):
    if request.method == 'POST':
        form = FormUserTICreationForm(request.POST)
        if form.is_valid():
            # Get form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            rol = form.cleaned_data['rol']
            area = form.cleaned_data['area']

            # Generar el nombre de usuario (username) si first_name y last_name no están vacíos
            if first_name and last_name:
                # Tomar la primera letra de first_name y el primer apellido de last_name
                username = f"{first_name[0].lower()}{last_name.split()[0]}"
            else:
                username = None

            try:
                # Create a new UserTI object
                nuevo_usuario_ti = UserTI.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    username=username,
                    rol=rol,
                    area=area
                )
                # Mensaje de éxito con el nombre de usuario
                messages.success(request, f'Usuario "{username}" creado exitosamente!')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = FormUserTICreationForm()

    return render(request, 'registro.html', {'form': form})


# views.py
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .forms import CambioContraseñaForm

def cambiar_contraseña(request):
    if request.method == 'POST':
        form = CambioContraseñaForm(request.POST)
        try:
            if form.is_valid():
                nueva_contraseña = form.cleaned_data['nueva_contraseña']
                confirmar_contraseña = form.cleaned_data['confirmar_contraseña']
                if nueva_contraseña != confirmar_contraseña:
                    messages.error(request, "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
                else:
                    usuario = form.cleaned_data['usuario']
                    # Establecer la nueva contraseña en el modelo de usuario
                    usuario.set_password(nueva_contraseña)
                    usuario.save()
                    # Redireccionar a alguna página de éxito
                    messages.success(request, f'Contraseña actualizada exitosamente!')
        except Exception as e:
            messages.error(request, f"Error al cambiar la contraseña: {e}")
    else:
        form = CambioContraseñaForm()
    return render(request, 'contraseña.html', {'form': form})



###################### VISTAS DE USUARIOS ####################################################3333
#vista para mostrar el index del usuario
def user_index(request):
    return render(request, 'user_index.html')

#vistas para dar de alta un servicio

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages

from random import choice

def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            nombre_solicitante = form.cleaned_data['nombreSolicitante']
            descripcion = form.cleaned_data['descripcion']
            area_solicitante = form.cleaned_data['areaSolicitante']
            problema = form.cleaned_data['problema']
            
            try:
                ultimo_servicio = Servicio.objects.latest('id')
                folio = 'TI{:04d}'.format(ultimo_servicio.id + 1)
            except ObjectDoesNotExist:
                folio = 'TI0001'  # Si no hay servicios, asignamos un folio inicial
            
            estado = 'abierto'
            
            area_problema = problema.nombre.lower()

            # Definir un mapeo de problemas a áreas correspondientes
            mapeo_problema_area = {
                'hardware': 'operaciones y servicios',
                'software': 'desarrollo de software',
                'conectividad a la red': 'redes y telecomunicaciones',
                'problemas de impresión': 'operaciones y servicios',
                'contraseñas': 'operaciones y servicios',
                'acceso a aplicaciones': 'operaciones y servicios',
                # Agrega más mapeos según sea necesario
            }
            nombre_area = mapeo_problema_area.get(area_problema)

            # Buscar todos los técnicos disponibles en el área correspondiente al problema
            usuarios_area_disponibles = UserTI.objects.filter(area__nombreArea__iexact=nombre_area, disponibilidad='disponible').order_by('cargaTrabajo')

            if usuarios_area_disponibles.exists():
                # Si hay técnicos disponibles en el área con disponibilidad "disponible", seleccionar al primero
                responsable = usuarios_area_disponibles.first()
            else:
                # Si no hay técnicos disponibles con disponibilidad "disponible", buscar al que tenga la menor carga de trabajo
                usuarios_area = UserTI.objects.filter(area__nombreArea__iexact=nombre_area).order_by('cargaTrabajo', 'disponibilidad')

                if usuarios_area.exists():
                    # Obtener a todos los técnicos con la menor carga de trabajo
                    min_carga_trabajo = usuarios_area.first().cargaTrabajo
                    usuarios_min_carga_trabajo = usuarios_area.filter(cargaTrabajo=min_carga_trabajo)

                    if usuarios_min_carga_trabajo.count() > 1:
                        # Si hay más de un técnico con la menor carga de trabajo, seleccionar uno de manera aleatoria
                        responsable = choice(usuarios_min_carga_trabajo)
                    else:
                        # Si solo hay un técnico con la menor carga de trabajo, seleccionarlo
                        responsable = usuarios_min_carga_trabajo.first()
                else:
                    # Si no hay técnicos disponibles en el área, seleccionar uno de manera aleatoria
                    responsable = UserTI.objects.order_by('?').first()

            # Aumentar la carga de trabajo del responsable en 1
            responsable.cargaTrabajo += 1
            responsable.save()
            
            servicio = Servicio.objects.create(
                folio=folio,
                nombreSolicitante=nombre_solicitante,
                descripcion=descripcion,
                responsable=responsable,
                problema=problema,
                areaSolicitante=area_solicitante,
                estado=estado,
                fechaCreacion=timezone.now(),
            )
            
            messages.success(request, '¡Servicio creado con éxito! En breve alguien se pondrá en contacto contigo.')
    else:
        form = ServicioForm()
    
    areas = Area.objects.all()
    problemas = Problema.objects.all()
    
    return render(request, 'servicio.html', {'form': form, 'areas': areas, 'problemas': problemas})
