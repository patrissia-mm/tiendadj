from django.urls import path, re_path
#
from . import views

app_name = 'venta_app'

urlpatterns = [
    path(
        'api/venta/reporte/',
        views.ReporteVentasList.as_view(),
        name = 'venta-reporte' 
    ),
    path(
        'api/venta/create/',
        views.RegistrarVenta.as_view(),
        name = 'venta-register' 
    ),
    path(
        'api/venta/add/',
        views.RegistrarVenta2.as_view(),
        name = 'venta-add' 
    ),
]
