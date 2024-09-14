from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Empleado

def index(request):
    return render(request, 'blog/index.html')

def autenticado_view(request):
    return render(request, 'blog/autenticado.html')

def calcular_pago(request):
    if request.method == 'POST':
        name_producto = str(request.POST['name_producto'])
        cantidad_productos = int(request.POST['cantidad_productos'])
        precio_por_unidad = int(request.POST['precio_por_unidad'])
        igv = 0.18
        descuento = 0.02

        total = calcular_pago_producto(cantidad_productos, precio_por_unidad)

        context = {
            'name_producto': name_producto,
            'cantidad_productos': cantidad_productos,
            'precio_por_unidad': precio_por_unidad,
            'igv': igv,
            'descuento': descuento,
            'total': total,
        }
        return render(request, 'blog/resultados.html', context)
    else:
        return render(request, 'blog/calcular_pago.html')

def calcular_pago_producto(cantidad_productos, precio_por_unidad):
    subtotal = cantidad_productos * precio_por_unidad
    igv = subtotal * 0.18
    descuento = subtotal * 0.02
    total_a_pagar=(subtotal+igv)-descuento
    return total_a_pagar

def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        # Verificar si los campos no están vacíos
        if not usuario or not password:
            return render(request, 'blog/login.html', {'error': 'Por favor, complete todos los campos.'})

        try:
            # Obtener el empleado basado en el nombre de usuario
            empleado = Empleado.objects.get(usuario=usuario)
            
            # Verificar la contraseña
            if check_password(password, empleado.password) or password == empleado.password:
                # Autenticar al usuario
                
                return redirect('autenticado')
            else:
                return render(request, 'blog/login.html', {'error': 'Contraseña incorrecta'})
        except Empleado.DoesNotExist:
            return render(request, 'blog/login.html', {'error': 'Usuario no encontrado'})
    else:
        return render(request, 'blog/login.html')
