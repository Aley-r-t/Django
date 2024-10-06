from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Evento
from django.contrib.auth.models import Permission,User

# Create your views here.

@login_required(login_url='eventos:login') 
def index(request):
    return render(request, 'eventos/index.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        # Recoger datos del formulario usando request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Iniciar sesión
            return redirect('eventos:index')  # Redirigir después de login exitoso
        else:
            # Pasar un mensaje de error si el login falla
            return render(request, 'eventos/login.html', {'error_message': 'Login fallido'})
    
    return render(request, 'eventos/login.html')


def register(request):
    if request.method == 'POST':
        # Recoger datos del formulario usando request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Crear un nuevo usuario
        user = User.objects.create_user(username=username, password=password)

        content_type = ContentType.objects.get_for_model(Evento)
        create_event_permission = Permission.objects.get(codename='create_eventos', content_type=content_type)
        edit_event_permission = Permission.objects.get(codename='edit_eventos', content_type=content_type)
        delete_event_permission = Permission.objects.get(codename='delete_eventos', content_type=content_type)
        view_event_permission = Permission.objects.get(codename='view_eventos', content_type=content_type)
        
        # Asignar los permisos al usuario
        user.user_permissions.add(create_event_permission)
        user.user_permissions.add(edit_event_permission)
        user.user_permissions.add(delete_event_permission)
        user.user_permissions.add(view_event_permission)
        
        return JsonResponse({'message': 'Usuario creado exitosamente'})
    
    return render(request, 'eventos/register.html')


def lista_eventos(request):
    eventos = Evento.objects.all()  # O filtra según el usuario si es necesario
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})

#Crear eventos
def crear_evento(request):
    if request.method == 'POST':
        # Recoger datos del formulario usando request.POST
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        ubicacion = request.POST.get('ubicacion')
        capacidad = request.POST.get('capacidad')
        
        # Crear un nuevo evento
        evento = Evento.objects.create(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, ubicacion=ubicacion, capacidad=capacidad)
        
        return JsonResponse({'message': 'Evento creado exitosamente'})
    render (request, 'eventos/crud_evento.html')

# Vista para cerrar sesión
def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect(reverse('eventos:login'))  # Redirige al login después del logout

