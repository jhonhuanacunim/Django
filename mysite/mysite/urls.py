"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import Despacho,Reporte,productos_vendidos,elimnarproveedor,hello,get_login,Editar,Compras,proveedores,Registrarse,Logeo,Salir,Nosotros,Productos,Carrito,Cantidad,eliminar_del_carrito,Admin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrarse/',Registrarse), #RUTA PARA REGISTRARSE
    path('home/',hello), #RUTA PRINCIPAL
    path('Logeo/',Logeo),   #RUTA PARA PODER LOGEARSE
    path('Salir/',Salir),
    path('',hello),
    path('Nosotros/',Nosotros),
    path('Productos/',Productos),
    path('carrito/',Carrito), #Ruta del carrito de compras /tabla
    path('cantidad/<int:id>',Cantidad), #Ruta para poder selecionar la cantidad
    path('eliminar/<int:detalle_id>', eliminar_del_carrito),
    path('eliminarproveedor/<int:proveedor_id>',elimnarproveedor),
    path('editar/<int:id>',Editar),
    path('administrador/',Admin),
    path('Compras/',productos_vendidos),
    path('proveedores/',proveedores),
    path('Reporte/',Reporte),
    path('Despacho/',Despacho),
    #path('login_page/',get_login),
 
]
