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
