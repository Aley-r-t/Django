from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.nombre

#Distrito añadido aqui rompiedo un poco las migraciones anteriores  
class Distrito(models.Model):
    nombre_dist = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_dist

class Cliente(models.Model):
    distrito = models.ForeignKey(Distrito, on_delete=models.SET_NULL, null=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.apellidos

# Modelo de Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    n_pedido = models.CharField(max_length=10, unique=True)
    fecha_pedido = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    igv = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.n_pedido
    

