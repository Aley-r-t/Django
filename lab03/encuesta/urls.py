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
]