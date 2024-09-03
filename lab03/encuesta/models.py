from django.db import models

# Create your models here.

class Pregunta(models.Model):
    pregunta_texto=models.CharField(max_length=100)
    pub_date=models.DateTimeField('fecha de publicacion')

class Opcion(models.Model):
    pregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_texto=models.CharField(max_length=100)
    votos=models.IntegerField(default=0)
