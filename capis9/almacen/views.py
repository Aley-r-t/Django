from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
import requests
from django.http import JsonResponse
# Create your views here.

class CategoriaListView(View):
    template_name = 'almacen/index.html'  # Plantilla para mostrar/crear/eliminar categorías

    
    def get(self, request, *args, **kwargs):
        categoria_id = kwargs.get('categoria_id')
        if categoria_id:  
            return self.get_categoria(request, categoria_id)

        
        return self.get_categorias(request)

    def get_categorias(self, request):
        url = "https://lab08-bpvy.onrender.com/categorias/"
        try:
            response = requests.get(url)
            response.raise_for_status()  
            categorias = response.json() 
        except requests.exceptions.RequestException as e:
            categorias = {"error": "Error al obtener datos del endpoint", "details": str(e)}

        
        return render(request, self.template_name, {'categorias': categorias})

    def get_categoria(self, request, categoria_id):
        url = f"https://lab08-bpvy.onrender.com/categorias/{categoria_id}/"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica que no haya errores
            categoria = response.json()  # Obtiene los datos JSON
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Error al obtener datos del endpoint", "details": str(e)}, status=500)

        return render(request, self.template_name, {'categoria': categoria})

    # Método POST para crear o eliminar categorías
    def post(self, request, *args, **kwargs):
        categoria_id = kwargs.get('categoria_id')  # Obtener el ID de la categoría desde kwargs
        method = request.POST.get('_method', '').upper()  # Detectar si es un DELETE simulado

        if method == 'DELETE':
            return self.post_delete(request, categoria_id)  # Llama a la función para eliminar
        else:
            return self.post_create(request)  # Llama a la función para crear

    def post_create(self, request):
        url = "https://lab08-bpvy.onrender.com/categorias/"  # URL para crear nuevas categorías
        name = request.POST.get('name')  

        if not name:
            return self.get_categorias(request)  # Devuelve las categorías con error

        data = {
            'name': name
        }

        try:
            # Envía los datos a la API
            response = requests.post(url, json=data)
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
        except requests.exceptions.RequestException as e:
            return self.get_categorias(request)  # Devuelve las categorías con error

        # Después de un POST exitoso, vuelve a renderizar la página con los datos actualizados
        return self.get_categorias(request)

    def post_delete(self, request, categoria_id):
        url = f"https://lab08-bpvy.onrender.com/categorias/{categoria_id}/"  # URL para eliminar categoría
        try:
            response = requests.delete(url)
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
            return redirect('index')  # Redirige a la vista donde se listan las categorías
        except requests.exceptions.RequestException as e:
            return self.get_categorias(request)  # Devuelve las categorías con error
        
class ProveedoresListView(View):
    template_name = 'almacen/provedores.html' 

    # Método GET para obtener proveedores o un proveedor específico
    def get(self, request, *args, **kwargs):
        proveedor_id = kwargs.get('proveedor_id')
        if proveedor_id:  
            return self.get_proveedor(request, proveedor_id)
        return self.get_proveedores(request)

    def get_proveedores(self, request):
        url = "https://lab08-bpvy.onrender.com/proveedores/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            proveedores = response.json()
        except requests.exceptions.RequestException as e:
            proveedores = {"error": "Error al obtener datos del endpoint", "details": str(e)}
        return render(request, self.template_name, {'proveedores': proveedores})

    def get_proveedor(self, request, proveedor_id):
        url = f"https://lab08-bpvy.onrender.com/proveedores/{proveedor_id}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            proveedor = response.json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Error al obtener datos del endpoint", "details": str(e)}, status=500)
        return render(request, self.template_name, {'proveedor': proveedor})

    # Método POST para crear, actualizar o eliminar proveedores
    def post(self, request, *args, **kwargs):
        proveedor_id = kwargs.get('proveedor_id')
        method = request.POST.get('_method', '').upper()
        
        if method == 'DELETE':
            return self.post_delete(request, proveedor_id)
        elif proveedor_id:  # Si hay un ID, actualizar proveedor
            return self.post_update(request, proveedor_id)
        else:
            return self.post_create(request)

    def post_create(self, request):
        url = "https://lab08-bpvy.onrender.com/proveedores/"
        name = request.POST.get('name')
        contact_info = request.POST.get('contact_info')

        if not name or not contact_info:
            return self.get_proveedores(request)

        data = {'name': name, 'contact_info': contact_info}
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return self.get_proveedores(request)
        return self.get_proveedores(request)

    def post_update(self, request, proveedor_id):
        url = f"https://lab08-bpvy.onrender.com/proveedores/{proveedor_id}/"
        name = request.POST.get('name')
        contact_info = request.POST.get('contact_info')
        
        if not name or not contact_info:
            return self.get_proveedores(request)

        data = {'name': name, 'contact_info': contact_info}
        try:
            response = requests.put(url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return self.get_proveedores(request)
        return self.get_proveedores(request)

    def post_delete(self, request, proveedor_id):
        url = f"https://lab08-bpvy.onrender.com/proveedores/{proveedor_id}/"
        try:
            response = requests.delete(url)
            response.raise_for_status()
            return redirect('proveedores')
        except requests.exceptions.RequestException as e:
            return self.get_proveedores(request)

class ProductoListView(View):
    template_name = 'almacen/productos.html'
    url_producto = "https://lab08-bpvy.onrender.com/productos/"
    categorias_url = "https://lab08-bpvy.onrender.com/categorias/"
    proveedores_url = "https://lab08-bpvy.onrender.com/proveedores/"

    def get(self, request, *args, **kwargs):
        producto_id = kwargs.get('producto_id')
        if producto_id:
            return self.get_producto(request, producto_id)
        return self.get_productos(request)

    def get_productos(self, request):
        try:
            
            response_productos = requests.get(self.url_producto)
            response_productos.raise_for_status()
            productos = response_productos.json()

            
            response_categorias = requests.get(self.categorias_url)
            response_categorias.raise_for_status()
            categorias = response_categorias.json()

            response_proveedores = requests.get(self.proveedores_url)
            response_proveedores.raise_for_status()
            proveedores = response_proveedores.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Error al obtener datos de la API", "details": str(e)}, status=500)

        return render(request, self.template_name, {
            'productos': productos,
            'categorias': categorias,
            'proveedores': proveedores
        })

    def get_producto(self, request, producto_id):
        try:
            
            url = f"{self.url_producto}{producto_id}/"
            response_producto = requests.get(url)
            response_producto.raise_for_status()
            producto = response_producto.json()

           
            response_categorias = requests.get(self.categorias_url)
            response_categorias.raise_for_status()
            categorias = response_categorias.json()

            response_proveedores = requests.get(self.proveedores_url)
            response_proveedores.raise_for_status()
            proveedores = response_proveedores.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Error al obtener datos del endpoint", "details": str(e)}, status=500)

        return render(request, self.template_name, {
            'producto': producto,
            'categorias': categorias,
            'proveedores': proveedores
        })

    def post(self, request, *args, **kwargs):
        producto_id = kwargs.get('producto_id')
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            return self.delete_producto(request, producto_id)
        elif producto_id:
            return self.update_producto(request, producto_id)
        else:
            return self.create_producto(request)

    def create_producto(self, request):
        data = {
            'nombre': request.POST.get('nombre'),
            'fecha_de_ingreso': request.POST.get('fecha_de_ingreso'),
            'cantidad_en_stock': request.POST.get('cantidad_en_stock'),
            'precio': request.POST.get('precio'),
            'categoria': int(request.POST.get('categoria')),
            'proveedor': int(request.POST.get('proveedor'))
        }

        try:
            response = requests.post(self.url_producto, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Error al crear el producto", "details": str(e)}, status=500)

        return redirect('productos')

    def update_producto(self, request, producto_id):
        url = f"{self.url_producto}{producto_id}/"
        data = {
            'nombre': request.POST.get('nombre'),
            'fecha_de_ingreso': request.POST.get('fecha_de_ingreso'),
            'cantidad_en_stock': request.POST.get('cantidad_en_stock'),
            'precio': request.POST.get('precio'),
            'categoria': int(request.POST.get('categoria')),
            'proveedor': int(request.POST.get('proveedor'))
        }

        try:
            response = requests.put(url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Error al actualizar el producto", "details": str(e)}, status=500)

        return redirect('productos')

    def delete_producto(self, request, producto_id):
        url = f"{self.url_producto}{producto_id}/"

        try:
            response = requests.delete(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Error al eliminar el producto", "details": str(e)}, status=500)

        return redirect('productos')

