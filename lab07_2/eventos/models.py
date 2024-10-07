from django.db import models
from django.contrib.auth.models import User  # Usaremos el modelo de Usuario de Django

# Modelo para representar un Evento
class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ubicacion = models.CharField(max_length=255)
    capacidad = models.PositiveIntegerField()
    
    class Meta:
        permissions = [
            ("create_eventos", "Puede crear eventos"),
            ("edit_eventos", "Puede editar eventos"),
            ("delete_eventos", "Puede eliminar eventos"),
            ("view_eventos", "Puede ver eventos"),
        ]

    def __str__(self):
        return self.nombre

# Modelo para representar los registros de usuarios a eventos
class RegistroEvento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='registros')
    asistencia = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} registrado en {self.evento.nombre}'

    class Meta:
        unique_together = ('usuario', 'evento')  # Un usuario solo puede registrarse una vez a un evento

