from django.urls import path
from . import views

app_name = 'desarrollo'

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('cursos/', views.filtrar_cursos, name='filtrar_cursos'),
]
