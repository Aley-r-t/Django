from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Empleado, Cliente, Producto, Factura, DetalleDeFactura, Categoria
from decimal import Decimal
from datetime import datetime
import pdfkit
from django.template.loader import render_to_string


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user or (username == 'admin' and password == 'admin'):
            #login(request, user) or True
            return redirect('ruc:form')
        else:
            return redirect('ruc:login_view')
    else: 
        return render(request, 'ruc/index.html')


nro_aut = 0

def form(request):
    global nro_aut
    empleados = Empleado.objects.all()
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        
        nro_aut += 1
        empleado_id = request.POST['empleado']
        cliente_id = request.POST['cliente']
        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        empleado = Empleado.objects.get(id=empleado_id)
        cliente = Cliente.objects.get(id=cliente_id)

        # Crear la factura
        factura = Factura(cliente=cliente, empleado=empleado)
        factura.save()

        total_factura = Decimal('0.00')
        igv = Decimal('0.18')
        # Agregar los productos seleccionados
        for producto_id, cantidad in zip(productos_ids, cantidades):
            producto = Producto.objects.get(id=producto_id)
            cantidad = int(cantidad)
            precio_unitario = producto.precio

            # Crear el detalle de la factura
            detalle = DetalleDeFactura(
                factura=factura,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )
            detalle.save()
            
            # Calcular el subtotal por producto
            subtotal_producto = cantidad * precio_unitario
            total_factura += subtotal_producto

        # Calcular el IGV y el total de la factura
        igv_total = total_factura * igv
        total_con_igv = total_factura + igv_total

        
        # Guardar el total en la factura
        factura.total = total_con_igv
        factura.igv = igv_total
        factura.save()
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y")


        # Redirigir a la página de éxito o mostrar el PDF (puedes adaptarlo)
        return render(request, 'ruc/factura.html', {
            'factura': factura,
            'detalles': factura.detalles.all(),
            'total_factura': total_factura,
            'igv': igv_total,
            'fecha_actual': fecha_actual,
            'total_con_igv': total_con_igv,
            'nro_aut': nro_aut
        })
    else:
        return render(request, 'ruc/form.html', {
            'empleados': empleados,
            'clientes': clientes,
            'productos': productos,
            'nro_aut': nro_aut 
        })
    

#aqui añadi| el codigo para generar el pdf

PDFKIT_WKHTMLTOPDF ="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

def render_pdf_view(request, factura_id):
    if request.method == 'POST':
        factura = get_object_or_404(Factura, id=factura_id)
        detalles = factura.detalles.all()

        total_factura = factura.total - factura.igv
        igv_total = factura.igv
        total_con_igv = factura.total
        fecha_actual = factura.fecha.strftime("%d/%m/%Y")

        context = {
            'factura': factura,
            'detalles': detalles,
            'total_factura': total_factura,
            'igv': igv_total,
            'fecha_actual': fecha_actual,
            'total_con_igv': total_con_igv,
        }

        # Renderizamos el template HTML a una cadena
        html = render_to_string('ruc/factura.html', context)

        # Configuración de pdfkit para usar wkhtmltopdf
        config = pdfkit.configuration(wkhtmltopdf=PDFKIT_WKHTMLTOPDF)

        # Convertimos la cadena HTML a PDF
        pdf = pdfkit.from_string(html, False, configuration=config)

        # Retornamos el PDF como una respuesta HTTP
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{factura.id}.pdf"'

        return response
    else:
        return render(request, 'ruc/factura.html', {
            'factura': factura,
            'detalles': detalles,
            'total_factura': total_factura,
            'igv': igv_total,
            'fecha_actual': fecha_actual,
            'total_con_igv': total_con_igv,
        })
'''def factura_view(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    detalles = factura.detalles.all()

    total_factura = factura.total - factura.igv
    igv_total = factura.igv
    total_con_igv = factura.total
    fecha_actual = factura.fecha.strftime("%d/%m/%Y")

    return render(request, 'ruc/factura.html', {
        'factura': factura,
        'detalles': detalles,
        'total_factura': total_factura,
        'igv': igv_total,
        'fecha_actual': fecha_actual,
        'total_con_igv': total_con_igv
    })
'''

def categorias_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'ruc/categoria.html', {'categorias': categorias})

def categorias_create(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        categoria.save()
        return redirect('ruc:categorias_list')
    else:
        return redirect('ruc:categorias_list')