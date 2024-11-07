"""
URL configuration for system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from system import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls), 

    path('gestionar_usuarios/', views.gestionar_usuario_cc, name='gestionar_usuario_cc'),

    path('login2/', views.ldap_login_view, name='ldap_login'),

    path('login/', views.ldap_login3_view, name='ldap_login3'),  # URL para la vista de inicio de sesión

    path('admin_index/' , views.admin_index,name='admin_index'),

    path('error/' , views.errores, name='error'),

    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar-sesion'),
    
    path('cerrar-sesion2/', views.cerrar_sesion2, name='cerrar-sesion2'),

    path('gestionar_area/', views.gestion_area, name='gestionar_area'),

    path('gestionar_problemas/', views.gestionar_problemas, name='gestionar_problemas'),

    path('crear_servicio/', views.crear_servicio_admin, name='crear_servicio_admin'),
   

    #Vista para que los del servicio soaicl puedan cerrar sus servicios
    path('actualizar_serv/' , views.actualizar_servicio_serv, name='actualizar_servicio_serv'),

    #que a la vez la vista de arriba hace uso de esta funcion para cambiar el estado de los servicios
    path('servicio/<int:servicio_id>/actualizar_servicio_social/', views.actualizar_estado_servicio_serv, name='actualizar_estado_servicio_serv'),


    path('csrf_error/', views.csrf_error_view, name='csrf_error'),
    
    path('crear_servicio_serv/', views.crear_servicio_serv, name='crear_servicio_serv'),
    
    path('solicitar_servicio/' , views.solicitar_servicio, name='solicitar_servicio_user'),
    ##prueba 2###

    path('dashboard_act/', views.servicios_dashboard, name='servicios_dashboard_act'),
    path('iniciar-atencion/<int:servicio_id>/', views.iniciar_atencion, name='iniciar_atencion'),
    path('finalizar/<int:servicio_id>/', views.finalizar_servicio, name='finalizar_servicio'),
    path('tomar/<int:servicio_id>/', views.tomar_servicio, name='tomar_servicio'),
    path('asignar/<int:servicio_id>/', views.asignar_servicio, name='asignar_servicio'),
    path('detalles_servicio/<int:servicio_id>/', views.detalles_servicio, name='detalles_servicio'),



    path('dashboard_actividades/', views.servicios_dashboard_serv, name='servicios_dashboard_serv'),
    path('iniciar_atencion_serv/<int:servicio_id>/', views.iniciar_atencion_serv, name='iniciar_atencion_serv'),
    path('finalizar_servicio/<int:servicio_id>/', views.finalizar_servicio_serv, name='finalizar_servicio_serv'),
    path('detalles_servicio/<int:servicio_id>/', views.detalles_servicio_serv, name='detalles_servicio_serv'),






]

