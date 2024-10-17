from django.shortcuts import render, redirect ,get_object_or_404
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
from django.db.models import Count, Q

# Create your views here.

@login_required(login_url='eventos:login') 
def index(request):
    # Obtener los parámetros de búsqueda desde la solicitud (GET)
    search_nombre = request.GET.get('nombre', '')
    search_fecha_inicio = request.GET.get('fecha_inicio', '')
    search_descripcion = request.GET.get('descripcion', '')
    asistencia_confirmada = request.GET.get('confirmada', '')

    # Subquery para obtener el primer registro de cada evento (el creador)
    subquery = RegistroEvento.objects.filter(evento=OuterRef('pk')).order_by('fecha_registro').values('usuario')[:1]

    # Empezar con todos los eventos
    eventos = Evento.objects.all()

    # Aplicar los filtros según los parámetros de búsqueda
    if search_nombre:
        eventos = eventos.filter(nombre__icontains=search_nombre)

    if search_fecha_inicio:
        eventos = eventos.filter(fecha_inicio__date=search_fecha_inicio)

    if search_descripcion:
        eventos = eventos.filter(descripcion__icontains=search_descripcion)

    # Filtrar eventos con asistencia confirmada si se selecciona el checkbox
    if asistencia_confirmada:
        eventos = eventos.filter(registros__asistencia=True)

    # Anotar el total de asistencias y el creador del evento
    eventos = eventos.annotate(
        total_asistencias=Count('registros', filter=Q(registros__asistencia=True)),
        creador_usuario=Subquery(subquery)  # Subquery para obtener el creador
    )

    eventos_data = []

    for evento in eventos:
        # Determinar si el usuario autenticado es el creador del evento
        es_creador = (evento.creador_usuario == request.user.id)

        # Verificar si el usuario es administrador o superusuario
        puede_modificar = request.user.is_staff or request.user.is_superuser or es_creador

        # Obtener el registro del evento si el usuario ya está registrado
        registro = RegistroEvento.objects.filter(evento=evento, usuario=request.user).first()

        # Añadir los datos a la lista eventos_data
        eventos_data.append({
            'evento': evento,
            'es_creador': es_creador,
            'puede_modificar': puede_modificar,  # Verificar si puede modificar o eliminar el evento
            'total_asistencias': evento.total_asistencias,  # Incluir el total de asistencias
            'registro': registro,  # Incluir el registro del usuario en el evento (si existe)
        })

    return render(request, 'eventos/index.html', {
        'eventos_data': eventos_data,
        'search_nombre': search_nombre,
        'search_fecha_inicio': search_fecha_inicio,
        'search_descripcion': search_descripcion,
        'asistencia_confirmada': asistencia_confirmada,  # Para mantener el estado del checkbox
    })

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
@login_required(login_url='eventos:login')
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
        # Maneja la asignación, revocación de permisos o eliminación de usuarios
        user_id = request.POST.get('user_id')
        permiso_id = request.POST.get('permiso_id')
        action = request.POST.get('action')  # 'otorgar', 'revocar', 'eliminar'

        usuario = User.objects.get(id=user_id)

        if action == 'otorgar':
            permiso = Permission.objects.get(id=permiso_id)
            usuario.user_permissions.add(permiso)

        elif action == 'revocar':
            permiso = Permission.objects.get(id=permiso_id)
            usuario.user_permissions.remove(permiso)

        elif action == 'eliminar':
            # Elimina al usuario solo si es superusuario
            if request.user.is_superuser:
                usuario.delete()

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

@login_required(login_url='eventos:login')
def confirmar_asistencia(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    registro, created = RegistroEvento.objects.get_or_create(usuario=request.user, evento=evento)

    confirmar = request.GET.get('confirmar')
    if confirmar == 'True':
        registro.asistencia = True
    else:
        registro.asistencia = False

    registro.save()
    return redirect('eventos:detalle_evento', evento_id=evento_id)

@login_required(login_url='eventos:login')    
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    numero_asistentes = obtener_numero_asistentes(evento)
    # ... otros datos del evento
    registro = RegistroEvento.objects.filter(usuario=request.user, evento=evento).first()
    return render(request, 'eventos/detalle_evento.html', {
        'evento': evento,
        'numero_asistentes': numero_asistentes,
        'registro': registro
    })

def obtener_numero_asistentes(evento):
    return RegistroEvento.objects.filter(evento=evento, asistencia=True).count()
# Vista para cerrar sesión
def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect(reverse('eventos:login'))  # Redirige al login después del logout

