from system import settings
import secrets
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from usuario.models import usuarioCC
from usuarioFEI.models import Area, Servicio, Problemas
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from system.forms import FormUsuarioCC, LoginForm, AltaAreaForm,ServicioForm, ProblemaForm, ServicioFormExtra, BajaAreaForm, BajaUsuarioForm, LoginForm2, BajaProblemaForm,LoginForm3
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CerrarServicioForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .forms import CambioContraseñaForm
from django.core.mail import send_mail
import random
import string
from django.db import transaction
from datetime import datetime, timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, timedelta
import ldap
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usuario.models import usuarioCC, Rol
from django.urls import reverse
from django.views.decorators.cache import never_cache




##################### VISTAS DE FUNCIONALIDADES ###############################################333
from functools import wraps
from django.shortcuts import redirect

def rol_requerido(rol_nombre):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not request.user.is_authenticated:
                return redirect('ldap_login')  # Redirige a la página de inicio de sesión si el usuario no ha iniciado sesión

            # Verificar si el usuario tiene el rol adecuado
            if not request.user.rol or request.user.rol.nombre != rol_nombre:
                # Si el usuario no tiene un rol o el rol no coincide, redirigir
                return redirect('error')  # Redirige a una página de error o la que prefieras

            # Si el usuario está autenticado y tiene el rol adecuado, ejecutar la vista original
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

######################## VISTA PARA MATAR LA COOKIE DE SESION DE LOS USUARIOS ##########################



def cerrar_sesion(request):
    logout(request)
    response = redirect('/login2/')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

#def cerrar_sesion(request):
#   logout(request)  
#   return redirect('/login2/')


def cerrar_sesion2(request):
    logout(request)
    response = redirect('/login/')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

#def cerrar_sesion2(request):
#    logout(request)  
#    return redirect('/login/')

############# VISTA PARA MOSTRAR LOS ERRORES DE USUARIO ###########
def errores(request):
    return render(request, 'errores.html')



########## vista de login para LDAP ############
def ldap_login_view(request):
    if request.method == 'POST':
        form = LoginForm2(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Verificar si el usuario existe en la base de datos de Django
            try:
                user = usuarioCC.objects.get(email=email)  # Cambiar User a usuarioCC
            except usuarioCC.DoesNotExist:
                # Si no está en la base de datos, mostrar error
                messages.error(request, 'El usuario no está registrado en el sistema.')
                return render(request, 'login2.html', {'form': form})

            # Si el usuario está en la base de datos, proceder con la autenticación LDAP
            LDAP_SERVER = 'ldap://148.226.12.10'  # Cambia a LDAPS si es necesario
            
            try:
                # Inicializar la conexión LDAP
                ldap_client = ldap.initialize(LDAP_SERVER)
                ldap_client.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
                ldap_client.set_option(ldap.OPT_REFERRALS, 0)
                ldap_client.simple_bind_s(email, password)

                # Autenticación exitosa en LDAP, iniciar sesión al usuario en Django
                login(request, user)

                # Redirigir según el rol del usuario
                if user.rol and user.rol.nombre == 'Técnico Académico':
                    return redirect('tec_index')
                elif user.rol and user.rol.nombre == 'Administrador':
                    return redirect('servicios_dashboard_act')
                elif user.rol and user.rol.nombre == 'Servicio Social':
                    return redirect('servicios_dashboard_act_serv')
                else:
                    messages.error(request, 'Rol de usuario no reconocido.')

            except ldap.INVALID_CREDENTIALS:
                messages.error(request, 'Credenciales inválidas. Por favor, intente de nuevo.')
            except ldap.SERVER_DOWN:
                messages.error(request, 'No se puede conectar al servidor LDAP.')
            except ldap.LDAPError as e:
                messages.error(request, f'Error LDAP: {str(e)}')
            finally:
                ldap_client.unbind()
    else:
        form = LoginForm2()

    return render(request, 'login2.html', {'form': form})

############## vista para el login de los usuarios que levantaran servicios #####
def ldap_login3_view(request):
    if request.method == 'POST':
        form = LoginForm2(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Excluir usuarios con el correo terminado en @estudiantes.uv.mx
           # if email.endswith('@estudiantes.uv.mx'):
           #     messages.error(request, 'El acceso está restringido para correos de estudiantes.')
           #     return render(request, 'login3.html', {'form': form})

            # Verificar si el usuario existe en la base de datos de Django
            try:
                user = usuarioCC.objects.get(email=email)  # Cambiar User a usuarioCC
            except usuarioCC.DoesNotExist:
                messages.error(request, 'El usuario no está registrado en el sistema.')

            # Conexión al servidor LDAP
            LDAP_SERVER = 'ldap://148.226.12.10'  # Cambia a LDAPS si es necesario
            
            try:
                # Inicializar la conexión LDAP
                ldap_client = ldap.initialize(LDAP_SERVER)
                ldap_client.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
                ldap_client.set_option(ldap.OPT_REFERRALS, 0)
                ldap_client.simple_bind_s(email, password)

                # Autenticación exitosa en LDAP, iniciar sesión al usuario en Django
                login(request, user)

                # Redirigir a user_index después de la autenticación exitosa
                return redirect('solicitar_servicio_user')

            except ldap.INVALID_CREDENTIALS:
                messages.error(request, 'Credenciales inválidas. Por favor, intente de nuevo.')
            except ldap.SERVER_DOWN:
                messages.error(request, 'No se puede conectar al servidor LDAP.')
            except ldap.LDAPError as e:
                messages.error(request, f'Error LDAP: {str(e)}')
            finally:
                ldap_client.unbind()

    else:
        form = LoginForm3()

    return render(request, 'login.html', {'form': form})

############## VISTA PARA TRATAR LOS ERRORES CSRF ########################3
def csrf_error_view(request):
    # Aquí puedes renderizar una página de error CSRF personalizada
    return render(request, 'csrf.html')




######################## VISTAS DE ADMINISTRADOR #######################################################

######################### VISTA PARA MOSTRAR EL INDEX DEL ADMINISTRADOR #####################333
@rol_requerido('Administrador')
@login_required(login_url='login2')
def admin_index(request):
    # Obtener el nombre de usuario del usuario autenticado
    username = request.user.username  # Obtiene el nombre de usuario

    # Pasar el nombre de usuario al contexto de la plantilla
    return render(request, 'admin_index.html', {'username': username})


#NUEVA ALTA DE AREA Y BAJA ################
@rol_requerido('Administrador')
@login_required(login_url='login2')
def gestion_area(request):
    # Obtener todas las áreas de la base de datos
    areas = Area.objects.all()

    # Manejo de las solicitudes POST para agregar o eliminar áreas
    if request.method == 'POST':
        area_nombre = request.POST.get('area')

        if 'alta-area' in request.POST and area_nombre:
            # Crear un nuevo área
            area = Area(nombre=area_nombre)
            area.save()
            messages.success(request, 'Área creada exitosamente!')
        
        elif 'baja-area' in request.POST and area_nombre:
            # Eliminar el área existente
            area = get_object_or_404(Area, nombre=area_nombre)
            area.delete()
            messages.success(request, 'Área eliminada exitosamente!')
        else:
            messages.error(request, 'No se ha podido procesar la solicitud.')

    return render(request, 'gestion_area.html', {'areas': areas})



######## vista para elimnar probelmas #####

@rol_requerido('Administrador')
@login_required(login_url='login2')
def gestionar_problemas(request):
    problemas = Problemas.objects.all()

    # Manejo del formulario para eliminar problema
    if request.method == 'POST':
        if 'eliminar' in request.POST:
            problema_id = request.POST.get('eliminar')
            problema = get_object_or_404(Problemas, id=problema_id)
            problema.delete()
            messages.success(request, 'Problema eliminado exitosamente!')
            return redirect('gestionar_problemas')  # Redirigir después de eliminar
        elif 'crear' in request.POST:
            nombre_problema = request.POST.get('nombre')
            if nombre_problema:
                Problemas.objects.create(nombre=nombre_problema)
                messages.success(request, 'Problema agregado exitosamente!')
                return redirect('gestionar_problemas')  # Redirigir después de agregar

    return render(request, 'gestionar_problemas.html', {'problemas': problemas})



### vista para dar de baja a user cc ###
@rol_requerido('Administrador')
@login_required(login_url='login2')
@login_required
def gestionar_usuario_cc(request):
    usuario_actual = request.user 
    if request.method == "POST":
        # Agregar usuario
        if 'alta-usuario' in request.POST:
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            rol_id = request.POST.get('rol')
            email = request.POST.get('email', '').strip()

            if first_name and last_name and email:
                generated_username = f"{first_name[0].lower()}{last_name.split()[0].lower()}"
                
                if not usuarioCC.objects.filter(username=generated_username).exists():
                    rol = Rol.objects.get(id=rol_id) if rol_id else None

                    nuevo_usuario = usuarioCC.objects.create_user(
                        username=generated_username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        rol=rol
                    )
                    
                    messages.success(request, "Usuario agregado exitosamente.")
                else:
                    messages.warning(request, "El usuario ya existe.")
            else:
                messages.error(request, "Por favor completa todos los campos obligatorios.")

        # Eliminar usuario
        elif 'baja-usuario' in request.POST:
            usuario_id = request.POST.get('usuario_id')
            try:
                usuario = usuarioCC.objects.get(id=usuario_id)
                usuario.delete()
                messages.success(request, f"Usuario {usuario.username} eliminado exitosamente.")
            except usuarioCC.DoesNotExist:
                messages.error(request, "El usuario no existe.")

    

    usuarios = usuarioCC.objects.all()
    roles = Rol.objects.all()
    context = {
        'usuarios': usuarios,
        'roles': roles,
    }
    return render(request, 'baja_usuario.html', context)


###vista para crear un servoicio siendo admin######

@rol_requerido('Administrador')
@login_required(login_url='login2')
def crear_servicio_admin(request):
    if request.method == 'POST':
        form = ServicioFormExtra(request.POST)
        
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            area_solicitante = form.cleaned_data['areaSolicitante']
            problema = form.cleaned_data['problema']

            # Asignar el username del usuario actual y responsable
            nombre_solicitante = request.user.username  # Obtener el username del usuario
            responsable = request.user  # Asignar el usuario actual como responsable

            # Crear el servicio con el nombre del solicitante, responsable y estado "en_atención"
            servicio = Servicio.objects.create(
                nombreSolicitante=nombre_solicitante,
                descripcion=descripcion,
                areaSolicitante=area_solicitante,
                problema=problema,
                responsable=responsable,  # Asignar el responsable 
                estado='asignado'  # Cambiar el estado a "en_atención"
            )

            # No es necesario llamar a servicio.save() aquí, ya que se guardó al crear
            messages.success(request, 'El servicio se creó exitosamente, recuerde que el servicio lo debe atender usted :).')

        else:
            messages.error(request, 'Hubo un error en el formulario.')
    else:
        form = ServicioForm()

    areas = Area.objects.all()
    problemas = Problemas.objects.all()

    return render(request, 'servicio_admin.html', {
        'form': form,
        'areas': areas,
        'problemas': problemas
    })


####prueba 2 de asignacion de servicios en cc ####

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@never_cache
@rol_requerido('Administrador')
@login_required(login_url='login2')
@requires_csrf_token
def servicios_dashboard(request):
    # Obtener el usuario actual
    usuario = request.user
    
    # Obtener los servicios asignados al usuario actual, excluyendo los que están en estado "finalizado"
    mis_servicios = Servicio.objects.filter(responsable=usuario).exclude(estado='finalizado')
    
    # Obtener los diferentes tipos de servicios
    solicitados = Servicio.objects.filter(estado='solicitado')
    asignados = Servicio.objects.filter(estado='asignado')
    en_atencion = Servicio.objects.filter(estado='en_atencion')
    finalizados = Servicio.objects.filter(estado='finalizado')


    # Obtener todos los usuarios para el modal de asignación
    usuarios = usuarioCC.objects.all()
    
    context = {
        'mis_servicios': mis_servicios,
        'solicitados': solicitados,
        'asignados': asignados,
        'en_atencion': en_atencion,
        'finalizados' : finalizados,
        'usuarios': usuarios,
    }
    
    return render(request, 'tomar2.html', context)

@rol_requerido('Administrador')
@login_required(login_url='login2')
@requires_csrf_token
def iniciar_atencion(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        servicio.estado = 'en_atencion'
        servicio.save()
        messages.success(request, 'Se ha iniciado la atención del servicio.')
    return redirect('servicios_dashboard_act')

@rol_requerido('Administrador')
@login_required(login_url='login2')
@requires_csrf_token
def finalizar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        comentarios = request.POST.get('comentarios')
        servicio.comentarios = comentarios
        servicio.estado = 'finalizado'
        servicio.fechaCierre = datetime.now()
        servicio.save()
        messages.success(request, 'El servicio ha sido finalizado exitosamente.')
    return redirect('servicios_dashboard_act')

@rol_requerido('Administrador')
@login_required(login_url='login2')
@requires_csrf_token
def tomar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        servicio.responsable = request.user
        servicio.estado = 'asignado'
        servicio.save()
        messages.success(request, f'Has tomado el servicio {servicio.folio}.')
    return redirect('servicios_dashboard_act')

@rol_requerido('Administrador')
@login_required(login_url='login2')
@requires_csrf_token
def asignar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        usuario_asignado = get_object_or_404(usuarioCC, id=usuario_id)
        servicio.responsable = usuario_asignado
        servicio.estado = 'asignado'
        servicio.save()
        messages.success(request, f'Servicio asignado a {usuario_asignado.username}.')
    return redirect('servicios_dashboard_act')


def detalles_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    return render(request, 'detalles.html', {'servicio': servicio})

################## VISTAS DE SERVICIO SOCIAL #################################

@rol_requerido('Servicio Social')
@login_required(login_url='login2')
def crear_servicio_serv(request):
    if request.method == 'POST':
        form = ServicioFormExtra(request.POST)
        
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            area_solicitante = form.cleaned_data['areaSolicitante']
            problema = form.cleaned_data['problema']

            # Asignar el username del usuario actual y responsable
            nombre_solicitante = request.user.username  # Obtener el username del usuario
            responsable = request.user  # Asignar el usuario actual como responsable

            # Crear el servicio con el nombre del solicitante, responsable y estado "en_atención"
            servicio = Servicio.objects.create(
                nombreSolicitante=nombre_solicitante,
                descripcion=descripcion,
                areaSolicitante=area_solicitante,
                problema=problema,
                responsable=responsable,  # Asignar el responsable 
                estado='asignado'  # Cambiar el estado a "en_atención"
            )

            # No es necesario llamar a servicio.save() aquí, ya que se guardó al crear
            messages.success(request, 'El servicio se creó exitosamente, recuerde que fue al ahcer esto el servicio lo debe atender usted :).')

        else:
            messages.error(request, 'Hubo un error en el formulario.')
    else:
        form = ServicioForm()

    areas = Area.objects.all()
    problemas = Problemas.objects.all()

    return render(request, 'servicio_serv.html', {
        'form': form,
        'areas': areas,
        'problemas': problemas
    })





@requires_csrf_token
@rol_requerido('Servicio Social')
@login_required(login_url='login2')
def actualizar_servicio_serv(request):
    # Obtener los servicios asignados al técnico
    servicios = Servicio.objects.filter(responsable=request.user)
    return render(request, 'actualizar_serv.html', {'servicios': servicios})

@requires_csrf_token
@rol_requerido('Servicio Social')
@login_required(login_url='login2')
def actualizar_estado_servicio_serv(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        servicio.estado = nuevo_estado
        
        # Si el estado es finalizado, guardar el comentario y la fecha de finalización
        if nuevo_estado == 'finalizado':
            comentarios = request.POST.get('comentarios')
            servicio.comentarios = comentarios  # Guardar comentarios en el servicio
            servicio.fechaCierre = datetime.now()  # Guardar la hora actual como fecha de finalización
            
        servicio.save()
        messages.success(request, f'Servicio {servicio.folio} ha sido actualizado.')

    return redirect('actualizar_servicio_serv')



###### gestion de servicios de servicio social
@requires_csrf_token
@never_cache
@login_required(login_url='login2')
@rol_requerido('Servicio Social')
def servicios_dashboard_serv(request):
    # Obtener el usuario actual
    usuario = request.user
    
    # Obtener los servicios asignados al usuario actual, excluyendo los que están en estado "finalizado"
    mis_servicios = Servicio.objects.filter(responsable=usuario).exclude(estado='finalizado')
    
    # Obtener los diferentes tipos de servicios
    solicitados = Servicio.objects.filter(estado='solicitado')
    asignados = Servicio.objects.filter(estado='asignado')
    en_atencion = Servicio.objects.filter(estado='en_atencion')
    finalizados = Servicio.objects.filter(estado='finalizado')


    # Obtener todos los usuarios para el modal de asignación
    usuarios = usuarioCC.objects.all()
    
    context = {
        'mis_servicios': mis_servicios,
        'solicitados': solicitados,
        'asignados': asignados,
        'en_atencion': en_atencion,
        'finalizados' : finalizados,
        'usuarios': usuarios,
    }
    
    return render(request, 'gestion_servicios.html', context)

@login_required
def iniciar_atencion_serv(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        servicio.estado = 'en_atencion'
        servicio.save()
        messages.success(request, 'Se ha iniciado la atención del servicio.')
    return redirect('servicios_dashboard_serv')

@login_required
def finalizar_servicio_serv(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        comentarios = request.POST.get('comentarios')
        servicio.comentarios = comentarios
        servicio.estado = 'finalizado'
        servicio.fechaCierre = datetime.now()
        servicio.save()
        messages.success(request, 'El servicio ha sido finalizado exitosamente.')
    return redirect('servicios_dashboard_serv')


def detalles_servicio_serv(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    return render(request, 'detalles.html', {'servicio': servicio})





###################### VISTAS DE USUARIOS ###################################################
#vistas para dar de alta un servicio
@never_cache
@login_required(login_url='ldap_login3')
def solicitar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        
        if form.is_valid():
            # Ya no es necesario hacer un .get() en estos casos
            nombre_solicitante = form.cleaned_data['nombreSolicitante']
            descripcion = form.cleaned_data['descripcion']
            area_solicitante = form.cleaned_data['areaSolicitante']  # Esto ya es un objeto Área
            problema = form.cleaned_data['problema']  # Esto ya es un objeto Problema

            # Crear el servicio
            servicio = Servicio.objects.create(
                nombreSolicitante=nombre_solicitante,
                descripcion=descripcion,
                areaSolicitante=area_solicitante,  # Ya es el objeto directamente
                problema=problema  # Ya es el objeto directamente
            )

            servicio.save()  # Guarda el nuevo servicio

            messages.success(request, 'El servicio se creó exitosamente.')
            

        else:
            messages.error(request, 'Hubo un error en el formulario.')

    else:
        form = ServicioForm()

    # Obtén las áreas y problemas para mostrarlos en el formulario
    areas = Area.objects.all()
    problemas = Problemas.objects.all()

    return render(request, 'servicio.html', {
        'form': form,
        'areas': areas,
        'problemas': problemas
    })


