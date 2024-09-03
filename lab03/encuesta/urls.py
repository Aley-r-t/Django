from django.urls import path
from . import views

app_name= 'encuesta'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pregunta_id>/', views.detalle, name='detalle'),
    path('<int:pregunta_id>/votar', views.votar, name='votar'),
]