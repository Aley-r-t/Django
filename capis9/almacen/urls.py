from django.urls import path
from .views import CategoriaListView, ProveedoresListView, ProductoListView


urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name='index'),
    path('categorias/<int:categoria_id>/', CategoriaListView.as_view(), name='categoria_detail'),

    path('proveedores/', ProveedoresListView.as_view(), name='proveedores'),
    path('proveedores/<int:proveedor_id>/', ProveedoresListView.as_view(), name='provedor_detail'),

    path('productos/', ProductoListView.as_view(), name='productos'),
    path('productos/<int:producto_id>/', ProductoListView.as_view(), name='producto_detail'),
   
]