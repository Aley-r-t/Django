from django.urls import path
from . import views

app_name= 'ruc'
urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('form/', views.form, name='form'),
    path('factura/<int:factura_id>/pdf/', views.render_pdf_view, name='render_pdf_view'),
    path('categorias/', views.categorias_list, name='categorias_list'),
    path('categoria/create/', views.categorias_create, name='categoria_create'),
   # path('factura/<int:factura_id>/', views.factura_view, name='factura_view'),
]