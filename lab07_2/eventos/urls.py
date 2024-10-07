from django.urls import path
from . import views


app_name='eventos'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('eventos/', views.crear_evento, name='crear_evento'),
    path('eventos/crear', views.crear_evento, name='crear_evento'),
    path('eventos/editar/<int:evento_id>/', views.actualizar_evento, name='actualizar_evento'), 
    path('gestionar_permisos/', views.gestionar_permisos, name='gestionar_permisos'), 
    path('evento/elimar/<int:evento_id>/', views.eliminar_evento,name='eliminar_evento'),
    path('eventos/<int:evento_id>/confirmar/', views.confirmar_asistencia, name='confirmar_asistencia'),
    path('eventos/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
]