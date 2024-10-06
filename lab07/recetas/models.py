from django.db import models

# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

class Receta(models.Model):
    titulo = models.CharField(max_length=100)
    ingredientes = models.TextField()
    preparacion = models.TextField()
    tiempo_registro = models.DateTimeField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    texto = models.TextField()
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comentario en {self.receta.titulo}'

