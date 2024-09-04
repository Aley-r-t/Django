from django.db import models

# Create your models here.

class Pregunta(models.Model):
    pregunta_texto=models.CharField(max_length=100)
    pub_date=models.DateTimeField('fecha de publicacion')

class Opcion(models.Model):
    pregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_texto=models.CharField(max_length=100)
    votos=models.IntegerField(default=0)

#Aqui añadi las ultimas migraciones
class Propietario(models.Model):
    nombre = models.CharField(max_length=100)
    numero_apartamento = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} - Apt: {self.numero_apartamento}"
    
class Vehiculo(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='vehiculos')

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.matricula})"

class Registro(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='registros')
    fecha_hora_entrada = models.DateTimeField('Fecha y hora de entrada')
    fecha_hora_salida = models.DateTimeField('Fecha y hora de salida', null=True, blank=True)

    def __str__(self):
        return f"Registro de {self.vehiculo} - Entrada: {self.fecha_hora_entrada}"
