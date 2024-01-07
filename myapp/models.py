from django.db import models
from django.contrib.auth.models import User


class project(models.Model):
    name= models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Task(models.Model):
    title= models.TextField(max_length=500)
    description=models.TextField(max_length=100)

    project=models.ForeignKey(project,on_delete=models.CASCADE)
    def __str__(self):
        return self.title + ' - ' + self.project.name
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)  # Agregamos un campo de dirección
    telefono = models.CharField(max_length=15)   # Agregamos un campo de teléfono
    rubroventa=models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
#Vegetales
class Vegetable(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.PositiveIntegerField()
    imagen_nombre = models.CharField(max_length=100)
    en_promocion = models.BooleanField(default=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    preciocompra=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre    
#Compras
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    direccion = models.CharField(max_length=100)  # Agregar el campo dirección

    
    def __str__(self):
        return f'Compra {self.id} por {self.usuario.username} el dia {self.fecha}'

# Modelo de Detalle de Compra
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    vegetal = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle de Compra #{self.compra.id} - {self.vegetal.nombre}'

# Modelo de Historial de Compras
class HistorialCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)

    def __str__(self):
        return f'Historial de Compra por {self.usuario.username}'

# Modelo de Carrito de Compras
class DetalleCarritoCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    vegetal = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f'Carrito de {self.usuario.username}'

# Modelo de Pagos
class Pago(models.Model):
    compra = models.OneToOneField(Compra, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pago de ${self.monto} para Compra {self.compra.id}'
    
    