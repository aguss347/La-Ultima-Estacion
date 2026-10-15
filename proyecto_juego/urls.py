from django.contrib import admin
from django.urls import path
from ultima_estacion import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.inicio, name="inicio"),
    path("mecanicas/", views.mecanicas, name="mecanicas"),
]
