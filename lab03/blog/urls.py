from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('autenticado/', views.autenticado_view, name='autenticado'),
    path('login/calcular_pago/', views.calcular_pago, name='calcular_pago'),
]