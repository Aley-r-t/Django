from django.contrib import admin

# Register your models here.
from .models import Categoria, Cliente, Distrito, Pedido
from .models import Producto

@admin.register(Categoria)
class RegistroCategoria(admin.ModelAdmin):
    list_display = ['nombre', 'pub_date']


def actualizar_stock_a_20(modeladmin, request, queryset):
    queryset.update(stock=20)
    modeladmin.message_user(request, "El stock ha sido actualizado a 20 para los productos seleccionados.")


@admin.register(Producto)
class RegistroProducto(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'pub_date']
    list_filter = ['categoria']
    search_fields = ['nombre']
    date_hierarchy = 'pub_date'
    actions = [actualizar_stock_a_20]
    #class Media:
     #   css = {
      #      'all': ('css/style.css',)
       # }

@admin.register(Distrito)
class RegistroDistrito(admin.ModelAdmin):
    list_display = ['nombre_dist', 'provincia', 'ciudad']
    search_fields = ['nombre_dist', 'provincia', 'ciudad']
    #date_hierarchy = 'fecha_publicacion'

@admin.register(Cliente)
class RegistroCliente(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'dni', 'telefono', 'direccion', 'email', 'fecha_nacimiento', 'fecha_publicacion']
    search_fields = ['nombres', 'apellidos', 'dni', 'email']
    date_hierarchy = 'fecha_publicacion'

@admin.register(Pedido)
class RegistroPedido(admin.ModelAdmin):
    list_display = ['cliente', 'n_pedido', 'fecha_pedido', 'monto', 'igv']
    search_fields = ['cliente', 'n_pedido']
    date_hierarchy = 'fecha_pedido'

