from django.shortcuts import render, redirect ,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.db import transaction 
from datetime import datetime 
from django.db.models import Subquery, OuterRef         
from .models import Evento, RegistroEvento
from django.utils import timezone
from django.contrib.auth.models import Permission,User

# Create your views here.

@login_required(login_url='eventos:login') 
def index(request):
    # Subquery para obtener el primer registro de cada evento (el creador)
    subquery = RegistroEvento.objects.filter(evento=OuterRef('pk')).order_by('fecha_registro').values('usuario')[:1]

    # Obtener todos los eventos con su primer registro (el creador)
    eventos = Evento.objects.annotate(creador_usuario=Subquery(subquery))

    eventos_data = []

    for evento in eventos:
        # Determinar si el usuario autenticado es el creador del evento
        es_creador = (evento.creador_usuario == request.user.id)

        # Añadir los datos a la lista
        eventos_data.append({
            'evento': evento,
            'es_creador': es_creador
        })

    return render(request, 'eventos/index.html', {'eventos_data': eventos_data})

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
        messages.success(request, 'Te has registrado correctamente incia sesión')
        return redirect('eventos:login')  # Redirigir al login después de registrarse
    return render(request, 'eventos/register.html')

#Crear eventos
def crear_evento(request):
    if request.method == 'POST': 
        return manejar_crear_evento(request)

    # Si es GET, renderiza el formulario para crear un nuevo evento
    return render(request, 'eventos/crud_evento.html', {'accion': 'crear'})

def manejar_crear_evento(request):
    # Asegúrate de que la solicitud es POST
    if request.method == 'POST':
        # Recoger datos del formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        ubicacion = request.POST.get('ubicacion')
        capacidad = request.POST.get('capacidad')

        # Convertir las fechas a timezone-aware
        if fecha_inicio:
            fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'))
        if fecha_fin:
            fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))

        try:
            with transaction.atomic():  # Iniciar una transacción
                # Crear un nuevo evento
                evento = Evento.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    ubicacion=ubicacion,
                    capacidad=capacidad, 
                )

                # Crear un registro para el usuario autenticado en el nuevo evento
                RegistroEvento.objects.create(
                    usuario=request.user,  # Asignar el usuario autenticado
                    evento=evento          # Asociar el nuevo evento
                )

            messages.success(request, 'Evento creado exitosamente')
        except Exception as e:
            messages.error(request, 'Error al crear el evento: {}'.format(str(e)))
        
        return redirect('eventos:index')
    else:
        messages.error(request, 'Error al crear el evento. Inténtalo de nuevo.')
        return redirect('eventos:index')

@login_required(login_url='eventos:login')    
def actualizar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    # Obtener el primer usuario que interactuó con el evento
    primer_interaccion = RegistroEvento.objects.filter(evento=evento).order_by('fecha_registro').first()
    primer_usuario = primer_interaccion.usuario if primer_interaccion else None

    es_creador = request.user == primer_usuario or request.user.is_superuser

    # Agregar condición para superusuarios
    if request.method == 'POST':
        if es_creador:
            return manejar_actualizar_evento(request, evento)       
        # ... lógica para permitir la edición
        return redirect('no_autorizado')
    else:
    # Si es GET, renderiza el formulario para editar el evento
        return render(request, 'eventos/crud_evento.html', {'accion': 'editar', 'evento': evento})

@login_required
@user_passes_test(lambda u: u.is_superuser)  # Solo permite a los superusuarios acceder
def gestionar_permisos(request):
    usuarios = User.objects.all()  # Obtiene todos los usuarios
    permisos = Permission.objects.all()  # Obtiene todos los permisos

    if request.method == 'POST':
        # Maneja la asignación o revocación de permisos
        user_id = request.POST.get('user_id')
        permiso_id = request.POST.get('permiso_id')
        action = request.POST.get('action')  # 'otorgar' o 'revocar'

        usuario = User.objects.get(id=user_id)
        permiso = Permission.objects.get(id=permiso_id)

        if action == 'otorgar':
            usuario.user_permissions.add(permiso)
        elif action == 'revocar':
            usuario.user_permissions.remove(permiso)

        return redirect('eventos:gestionar_permisos')

    return render(request, 'eventos/gestionar_permisos.html', {
        'usuarios': usuarios,
        'permisos': permisos,
    })

def manejar_actualizar_evento(request, evento):
    # Recoger datos del formulario usando request.POST
    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')
    fecha_inicio = request.POST.get('fecha_inicio')
    fecha_fin = request.POST.get('fecha_fin')
    ubicacion = request.POST.get('ubicacion')
    capacidad = request.POST.get('capacidad')

    # Actualizar los campos del evento
    evento.nombre = nombre
    evento.descripcion = descripcion
    evento.fecha_inicio = fecha_inicio
    evento.fecha_fin = fecha_fin
    evento.ubicacion = ubicacion
    evento.capacidad = capacidad
    evento.save()  # Guardar cambios en el evento existente

    messages.success(request, 'Editado correctamente')

    return redirect('eventos:index')
#Ultima parte
@login_required(login_url='eventos:login')
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    primer_interaccion = RegistroEvento.objects.filter(evento=evento).order_by('fecha_registro').first()
    primer_usuario = primer_interaccion.usuario if primer_interaccion else None

    es_creador = request.user == primer_usuario or request.user.is_superuser
    # Verificar si el usuario es el creador del evento o tiene los permisos necesarios
   
    # Pantalla de confirmación (opcional)
    if request.method == 'POST':
        if es_creador:
            evento.delete()
            messages.success(request, 'Eliminaste Correctamente')
            return redirect('eventos:index')
    else:
        return render(request, 'eventos/index.html')

# Vista para cerrar sesión
def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect(reverse('eventos:login'))  # Redirige al login después del logout

