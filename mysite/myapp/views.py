from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .models import Vegetable,DetalleCarritoCompra,Compra,DetalleCompra,Proveedor  # Importa tu modelo Usuarios
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models import Sum,Count
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from collections import defaultdict

def Despacho(request):
    compras = Compra.objects.all()  # Obtener todas las compras (ajusta esto según tu lógica)
    return render(request, 'despacho.html', {'compras': compras})

def Reporte(request):
    # Calcular la fecha actual y la fecha de una semana atrás
    fecha_actual = datetime.now()
    fecha_semana_anterior = fecha_actual - timedelta(days=7)
    total_amount = 0
    total_ganancia=0
    total_vegetables = 0  # Variable para almacenar el total de productos
    # Filtrar las compras realizadas en la última semana
    compras_semana_pasada = Compra.objects.filter(fecha__range=[fecha_semana_anterior, fecha_actual])

    # Crear una lista para almacenar las verduras de las compras de la última semana con cantidad vendida y subtotal
    verduras_semana_pasada = []

    for compra in compras_semana_pasada:
        detalles_compra = DetalleCompra.objects.filter(compra=compra)
        for detalle in detalles_compra:
            verdura = detalle.vegetal
            cantidad_vendida = detalle.cantidad
            subganancia=(detalle.vegetal.precio -detalle.vegetal.preciocompra)*detalle.cantidad
            subtotal = detalle.subtotal
            # Verificar si la verdura ya se encuentra en la lista
            found = False
            for v in verduras_semana_pasada:
                if v['verdura'] == verdura:
                    v['cantidad_vendida'] += cantidad_vendida
                    v['subtotal'] += subtotal
                    v['subganancia']+= subganancia
                    found = True
                    break

            if not found:
                verduras_semana_pasada.append({
                    'verdura': verdura,
                    'cantidad_vendida': cantidad_vendida,
                    'subtotal': subtotal,
                    'subganancia':subganancia,
                })
            total_amount += subtotal
            total_ganancia +=subganancia
        # Crear un diccionario para mantener un seguimiento de la cantidad vendida de cada verdura
    cantidad_vendida_verduras = defaultdict(int)

    # Iterar sobre las verduras y rastrear la cantidad vendida de cada una
    if verduras_semana_pasada:
        for verdura_info in verduras_semana_pasada:
            verdura = verdura_info['verdura']
            cantidad_vendida = verdura_info['cantidad_vendida']
            cantidad_vendida_verduras[verdura] += cantidad_vendida
        verdura_mas_vendida = max(cantidad_vendida_verduras, key=cantidad_vendida_verduras.get)
        cantidad_mas_vendida = cantidad_vendida_verduras[verdura_mas_vendida]
    # Encontrar la verdura más vendida basada en la cantidad vendida
    else:
        verdura_mas_vendida = None
        cantidad_mas_vendida = 0

    # Calcular el total de productos y la cantidad disponible
    total_vegetables = Vegetable.objects.aggregate(total=Count('id'))['total']
    cantidad_disponible = Vegetable.objects.aggregate(total=Sum('cantidad_disponible'))['total']
    # Añade estas líneas para imprimir los valores y verificar la estructura de datos
    print("Verduras semana pasada:", verduras_semana_pasada)
    print("Total de verduras:", total_vegetables)
    print("Cantidad disponible:", cantidad_disponible)
    return render(request, 'reporte.html', {
        'verduras_semana_pasada': verduras_semana_pasada,
        'total_amount': total_amount,
        'total_ganancia': total_ganancia,
        'total_vegetables': total_vegetables,
        'cantidad_disponible': cantidad_disponible,
        'verdura_mas_vendida': verdura_mas_vendida,
        'cantidad_mas_vendida': cantidad_mas_vendida,
    })


def Compras(request):
    return render(request, 'compras.html')

def proveedores(request):
    if request.method =='GET':
        proveedores = Proveedor.objects.all()  # Recupera todos los objetos Proveedor
        return render(request, 'Proveedores.html', {'proveedores': proveedores})
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        rubro = request.POST.get('rubroventa')

        # Crea un nuevo objeto Proveedor y guárdalo en la base de datos
        proveedor = Proveedor(nombre=nombre, direccion=direccion, telefono=telefono,rubroventa=rubro)
        proveedor.save()

        return redirect('/proveedores/')     
def productos_vendidos(request):
    detalles_compra = DetalleCompra.objects.all()

    # Crear un diccionario para el conteo de productos vendidos
    conteo_productos_vendidos = {}
    total_amount = Decimal('0.00')  # Inicializa el total_amount como Decimal

    for detalle in detalles_compra:
        vegetal = detalle.vegetal
        if vegetal in conteo_productos_vendidos:
            conteo_productos_vendidos[vegetal] += detalle.cantidad
        else:
            conteo_productos_vendidos[vegetal] = detalle.cantidad

        # Calcula el subtotal y suma al total_amount
        subtotal = vegetal.precio * detalle.cantidad
        total_amount += subtotal

    # Obtener la lista de productos vendidos
    productos_vendidos = []
    for vegetal, cantidad in conteo_productos_vendidos.items():
        productos_vendidos.append({'producto': vegetal, 'cantidad': cantidad})

    return render(request, 'compras.html', {'productos_vendidos': productos_vendidos, 'total_amount': total_amount})

def eliminar_del_carrito(request, detalle_id):
    detalle = get_object_or_404(DetalleCarritoCompra, id=detalle_id)

    # Elimina el detalle del carrito
    detalle.delete()

    # Redirige al usuario de vuelta al carrito de compras
    return redirect('/carrito/')
def elimnarproveedor(request,proveedor_id):
    proveedor=get_object_or_404(Proveedor,id=proveedor_id)
    proveedor.delete()
    return redirect('/proveedores/')
    return
def Admin(request):
    return render(request, 'cantidad.html')
@login_required(login_url='/Logeo/')
def Editar(request, id):
    if request.method =='GET':
        detalles_carrito = DetalleCarritoCompra.objects.get(id=id)
        return render(request, 'editar.html', {'detalles_carrito': detalles_carrito})

    if request.method == 'POST':
        detalles_carrito = DetalleCarritoCompra.objects.get(id=id)
        nueva_cantidad = int(request.POST['nueva_cantidad'])

        if nueva_cantidad >= 0:
            detalles_carrito.cantidad = nueva_cantidad
            detalles_carrito.subtotal = detalles_carrito.vegetal.precio * nueva_cantidad
            detalles_carrito.save()
            return redirect('/carrito/')

    

@login_required(login_url='/Logeo/')
def Cantidad(request,id):
    if request.method =='GET':
        Vegetable.objects.get(id=id)
        return render(request, 'cantidad.html', {'Vegetable': Vegetable.objects.get(id=id)})
    else:
        cantidad_comprada = int(request.POST['cantidad_comprada'])
        vegetal = Vegetable.objects.get(id=id)
        if cantidad_comprada > 0 and cantidad_comprada <= vegetal.cantidad_disponible:
            
            subtotal = vegetal.precio * cantidad_comprada
#******     # Restar la cantidad comprada a la cantidad disponible ******IMPORTANTEEE*******
            # vegetal.cantidad_disponible -= cantidad_comprada
            # vegetal.save()
            DetalleCarritoCompra.objects.create(usuario=request.user, vegetal=vegetal, cantidad=cantidad_comprada, subtotal=subtotal)

            return redirect('/Productos/')
        else:
            #ERROR PRODUCTOS INSUFICIENTES
            return render(request, 'cantidad.html', {'Vegetable': Vegetable.objects.get(id=id)})
        
    
# Create your views here.
def Carrito(request):
    if request.method =='GET':
        detalles_carrito = DetalleCarritoCompra.objects.filter(usuario=request.user)
        total_amount = sum([detalle.subtotal for detalle in detalles_carrito])
        return render(request, 'carrito.html', {'detalles_carrito': detalles_carrito,'total_amount': total_amount})
    else:
        detalles_carrito = DetalleCarritoCompra.objects.filter(usuario=request.user)
            # Crear una nueva compra y detalles de compra para cada elemento en el carrito
        direccion = request.POST.get('direccion')  # Obtener la dirección del formulario
        nueva_compra = Compra.objects.create(usuario=request.user, direccion=direccion)  # Agregar la dirección a la compra
        for detalle_carrito in detalles_carrito:
            DetalleCompra.objects.create(
                compra=nueva_compra,
                vegetal=detalle_carrito.vegetal,
                cantidad=detalle_carrito.cantidad,
                precio_unitario=detalle_carrito.vegetal.precio,
                subtotal=detalle_carrito.subtotal
            )
            detalle_carrito.vegetal.cantidad_disponible -= detalle_carrito.cantidad
            detalle_carrito.vegetal.save()

        # Borra todos los detalles del carrito asociados al usuario
        detalles_carrito.delete()

        return redirect('/home/')



def Productos(request):
    productos=Vegetable.objects.all() #poner tabla verduras
    return render(request,'productos.html', {
        'Productos' :productos   #Importa el que esta en comillas para templates
    })
def Nosotros(request):
    return render(request,'nosotros.html')
def Salir(request):
    logout(request)
    return redirect('/home/')
def Registrarse(request):
    if request.method =='GET':
       
        return render(request,'registrarse.html',{
        'form':UserCreationForm
    })
    else:
        if request.POST['password1'] ==request.POST['password2']:
            #Registrar usuario
            try:
                user =User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('/Logeo/') 
            except IntegrityError:
                return render(request,'index.html',{
                'form':UserCreationForm,
                "error":"Usuario ya existe"
                    }) 
                
        return render(request,'index.html',{
            'form':UserCreationForm,
            "error":'Contras no coinciden'
             }) 
def tasks(request):
    return render(request,'index.html')
            
def Logeo(request):
    if request.method=='GET':
            return render(request,'logeo.html',{
        'form':AuthenticationForm
        
    })
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST
        ['password'])
        if user is None:
            return render(request,'logeo.html',{
            'form':AuthenticationForm,
            'error':'Username or password is incorrect'
    })
        else:
            login(request,user)
            
            return redirect('/home/')            
            
            
            
def get_login(request):
    return render(request,'login_page.html')

def hello(request):
    productos=Vegetable.objects.all() #poner tabla verduras
    return render(request,'index.html', {
        'Productos' :productos   #Importa el que esta en comillas para templates
    })

