from django.contrib import admin
from .models import project,Task,Vegetable,Pago,HistorialCompra,Compra,DetalleCompra

# Register your models here.

admin.site.register(DetalleCompra)
admin.site.register(Pago)
admin.site.register(Compra)
admin.site.register(HistorialCompra)
#admin.site.register()

admin.site.register(Vegetable)