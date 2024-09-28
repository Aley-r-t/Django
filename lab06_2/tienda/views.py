from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Producto, Categoria


# Create your views here.


def index(request):
    product_list = Producto.objects.order_by('nombre')[:6]
    categoria_list = Categoria.objects.values('nombre').distinct()
    context = {'product_list': product_list, 'categoria_list': categoria_list}
    return render(request, 'tienda/index.html', context)

def producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    categoria_list = Categoria.objects.values('nombre').distinct()
    context = {'producto': producto, 'categoria_list': categoria_list}
    return render(request, 'tienda/producto.html',context)

def categoria(request, categoria_nombre):
    categorias = Categoria.objects.filter(nombre=categoria_nombre)
    
    if not categorias.exists():
        raise Http404("No se encontró ninguna categoría con ese nombre.")
    
    categoria = categorias.first()
    product_list = Producto.objects.filter(categoria=categoria)
    product_count = product_list.count() 
    categoria_list = Categoria.objects.values('nombre').distinct()
    context = {
        'categoria': categoria,
        'product_list': product_list,
        'product_count': product_count,  
        'categoria_list': categoria_list
    }
    # Renderiza la plantilla con el contexto
    return render(request, 'tienda/categoria.html', context)


