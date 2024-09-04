from django.shortcuts import render,redirect, get_object_or_404
from .models import Opcion, Pregunta, Vehiculo,Propietario, Registro
from django.contrib import messages


# Create your views here.
def index(request):
    Lista_de_preguntas=Pregunta.objects.order_by('-pub_date')
    context={'question_list':Lista_de_preguntas}
    return render(request, 'encuesta/index.html', context)

def detalle(request, pregunta_id):
    pregunta=Pregunta.objects.get(pk=pregunta_id)
    context={'pregunta':pregunta}
    return render(request, 'encuesta/detalle.html', context)

def votar(request,pregunta_id):
    pregunta = Pregunta.objects.get(pk=pregunta_id)
    opcionSeleccionada = pregunta.opcion_set.get(pk=request.POST['opcion'])
    opcionSeleccionada.votos += 1
    opcionSeleccionada.save()
    context = {'pregunta': pregunta}
    return render(request, 'encuesta/resultado.html', context)

def autos(request):
    return render(request, 'encuesta/autos.html')

#aqui se añadio 

def propietarios(request):
    lista_propietarios = Propietario.objects.all()
    context = {'propietarios_list': lista_propietarios}
    return render(request, 'encuesta/propietarios.html', context)
    
# Aqui ponemos el crud de propietarios

def crear_propietario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        numero_apartamento = request.POST['numero_apartamento']
        telefono = request.POST['telefono']
        email = request.POST['email']
        propietario = Propietario(nombre=nombre,numero_apartamento=numero_apartamento, telefono=telefono, email=email)
        propietario.save()
        return render(request, 'encuesta/crear_propietarios.html', {'mensaje': 'Propietario creado correctamente'})
    else:
        return render(request, 'encuesta/crear_propietarios.html')

def editar_propietario(request, propietario_id):
    propietario = get_object_or_404(Propietario, pk=propietario_id)
    if request.method == 'POST':
        propietario.nombre = request.POST['nombre']
        propietario.numero_apartamento = request.POST['numero_apartamento']
        propietario.telefono = request.POST['telefono']
        propietario.email = request.POST['email']
        propietario.save()
        return render(request, 'encuesta/editar_propietarios.html', {'mensaje': 'Propietario actualizado correctamente'})
    else:
        return render(request, 'encuesta/editar_propietarios.html', {'propietario': propietario})

def eliminar_propietario(request, propietario_id):
    propietario = get_object_or_404(Propietario, pk=propietario_id)
    propietario.delete()
    return render(request, 'encuesta/pro_delete.html', {'mensaje': 'Propietario eliminado correctamente'})

# Aqui ponemos el crud de vehiculos
def lista_vehiculos(request):
    vehiculos = Vehiculo.objects.select_related('propietario').all()
    return render(request, 'encuesta/lista_vehiculos.html', {'vehiculos': vehiculos})

def crear_vehiculo(request):
    if request.method == 'POST':
        matricula = request.POST['matricula']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        color = request.POST['color']
        propietario_id = request.POST['propietario']
        propietario = Propietario.objects.get(pk=propietario_id)
        vehiculo = Vehiculo(matricula=matricula, marca=marca, modelo=modelo, color=color, propietario=propietario)
        vehiculo.save()
        return render(request, 'encuesta/crear_vehiculo.html', {'mensaje': 'Vehiculo creado correctamente'})
    else:
        propietarios = Propietario.objects.all()
        return render(request, 'encuesta/crear_vehiculo.html', {'propietarios': propietarios})

def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        vehiculo.matricula = request.POST['matricula']
        vehiculo.marca = request.POST['marca']
        vehiculo.modelo = request.POST['modelo']
        vehiculo.color = request.POST['color']
        propietario_id = request.POST['propietario']
        propietario = Propietario.objects.get(pk=propietario_id)
        vehiculo.propietario = propietario
        vehiculo.save()
        return render(request, 'encuesta/editar_vehiculo.html', {'mensaje': 'Vehiculo actualizado correctamente'})
    else:
        propietarios = Propietario.objects.all()
        return render(request, 'encuesta/editar_vehiculo.html', {'vehiculo': vehiculo, 'propietarios': propietarios})
    
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    vehiculo.delete()
    return render(request, 'encuesta/vehiculo_delete.html', {'mensaje': 'Vehiculo eliminado correctamente'})