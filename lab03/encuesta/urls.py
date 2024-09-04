from django.urls import path
from . import views

app_name= 'encuesta'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pregunta_id>/', views.detalle, name='detalle'),
    path('<int:pregunta_id>/votar', views.votar, name='votar'),
    path('autos/', views.autos, name='autos'),
    path('propietarios/', views.propietarios, name='propietarios'),
    path('crear_propietario/', views.crear_propietario, name='crear_propietario'),
    path('editar_propietario/<int:propietario_id>', views.editar_propietario, name='editar_propietario'),
    path('eliminar_propietario/<int:propietario_id>', views.eliminar_propietario, name='eliminar_propietario'),
    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('crear_vehiculo/', views.crear_vehiculo, name='crear_vehiculo'),
    path('editar_vehiculo/<int:vehiculo_id>', views.editar_vehiculo, name='editar_vehiculo'),
    path('eliminar_vehiculo/<int:vehiculo_id>', views.eliminar_vehiculo, name='eliminar_vehiculo'),
]