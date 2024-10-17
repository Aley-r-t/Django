from django.shortcuts import render
from .models import Curso, Semestre
# Create your views here.
def index(request):
    return render(request, 'desarrollo/index.html')

def lista_cursos(request):
    cursos = Curso.objects.all()  # Obtenemos todos los cursos
    return render(request, 'desarrollo/index.html', {'cursos': cursos})

def filtrar_cursos(request):
    # Obtener todos los semestres
    semestres = Semestre.objects.all()

    # Filtrar cursos según el semestre seleccionado
    semestre_seleccionado = request.GET.get('semestre')  # Obtener semestre de la query string
    cursos = Curso.objects.all()  # Obtener todos los cursos inicialmente

    if semestre_seleccionado:
        cursos = cursos.filter(semestre_id=semestre_seleccionado)  # Filtrar por semestre

    return render(request, 'desarrollo/filtrar_cursos.html', {
        'cursos': cursos,
        'semestres': semestres,
        'semestre_seleccionado': semestre_seleccionado,
    })
