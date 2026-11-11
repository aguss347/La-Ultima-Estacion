from django.contrib import admin
from django.urls import path
from ultima_estacion import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("registro/", views.registro, name="registro"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("usuarios/pdf/", views.descargar_usuarios_pdf, name="usuarios_pdf"),
    path("", views.inicio, name="inicio"),
    path("mecanicas/", views.mecanicas, name="mecanicas"),
    path("desarrollo/", views.pagina, name="pagina"),
    path("contacto/", views.contacto, name="contacto"),
]
