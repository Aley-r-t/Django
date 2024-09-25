from django.urls import path
from . import views

app_name= 'ruc'
urlpatterns = [
    path('', views.index, name='index'),
    path('pdf/', views.login_view, name='login_view'),


]