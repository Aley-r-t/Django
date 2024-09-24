from django.db import models

# Create your models here.

# Modelo de Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ruc = models.CharField(max_length=13, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

# Modelo de Empleado
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

# Modelo de Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')  # Relación con Categoría

    def __str__(self):
        return self.nombre

# Modelo de Factura
class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con cliente
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)  # Relación con empleado
    fecha = models.DateTimeField(auto_now_add=True)
    igv = models.DecimalField(max_digits=10, decimal_places=2, default=0.18)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Factura {self.id} - {self.fecha} - Cliente: {self.cliente.nombre}'

# Modelo de Detalle de Factura
class DetalleDeFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')  # Relación con factura
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con producto
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle de Factura {self.factura.id} - Producto {self.producto.nombre}'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
