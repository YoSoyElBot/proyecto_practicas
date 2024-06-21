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

    path('registro/' , views.crear_usuario_ti, name='registro'),

    path('login/' , views.login_view, name='login'),

    path('tec_index/' , views.tec_index,name='tec_index'),

    path('admin_index/' , views.admin_index,name='admin_index'),

    path('error/' , views.errores, name='error'),

    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar-sesion'),

    path('alta_area/' , views.alta_area, name='alta-area'),

    path('agregar/' , views.agregar_usuario, name='agregar'),

    path('' , views.user_index, name= 'user_index'),

    path('user_index/' , views.user_index, name= 'user_index'),

    path('servicio/' , views.crear_servicio, name='crear_servicio'),

    path('alta_problemas/' , views.alta_problemas, name='alta_problemas'),

    path('dashboard/' , views.dashboard_tecnico, name='dashboard_tecnico'),

    path('cerrar/' , views.cerrar_servicio, name='cerrar_servicio'),

    path('servicios_abiertos/', views.servicios_abiertos),

    path('servicios_cerrados/' , views.servicios_cerrados),

    path('supervisor_index/' , views.supervisor_index, name='supervisor_index'),

    path('tecnicos/' , views.ver_tecnicos),

    path('cambio_contraseña/', views.cambiar_contraseña, name='csrf_error'),

    path('csrf_error/', views.csrf_error_view, name='csrf_error'),
]
