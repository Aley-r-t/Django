from django.urls import path
from . import views

app_name= 'ruc'
urlpatterns = [
    path('', views.index, name='index'),
]