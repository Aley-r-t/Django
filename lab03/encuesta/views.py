from django.shortcuts import render
from .models import Opcion, Pregunta

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

