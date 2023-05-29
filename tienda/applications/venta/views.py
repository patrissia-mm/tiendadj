from django.shortcuts import render
from django.utils import timezone
#
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView
)
#
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
#
from applications.producto.models import Product
from .models import Sale, SaleDetail
from .serializers import (
    VentaReporteSerializers,
    ProcesoVentaSerializer,
    ProcesoVentaSerializer2
)

class ReporteVentasList(ListAPIView):

    serializer_class = VentaReporteSerializers

    def get_queryset(self):
        return Sale.objects.all()

class RegistrarVenta(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    serializer_class = ProcesoVentaSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProcesoVentaSerializer(data = request.data)
        #
        serializer.is_valid(raise_exception=True)
        #
        venta = Sale.objects.create(
            date_sale = timezone.now(),
            amount = 0,
            count = 0,
            type_invoce = serializer.validated_data['type_invoce'],
            type_payment = serializer.validated_data['type_payment'],
            adreese_send = serializer.validated_data['adreese_send'],
            user = self.request.user,
        )
        #variables para venta
        amount=0 #monto total de venta
        count=0
        #recuperamos los productos de la venta
        productos = serializer.validated_data['productos']
        #
        ventas_detalle = []
        #
        for producto in productos:
            prod = Product.objects.get(id=producto['pk'])
            venta_detalle = SaleDetail(
                sale = venta,
                product = prod,
                count = producto['count'],
                price_purchase = prod.price_purchase,
                price_sale = prod.price_sale,
            )
            amount = amount + producto['count'] * prod.price_sale
            count = count + producto['count']
            ventas_detalle.append(venta_detalle)
        
        venta.amount = amount
        venta.count = count
        venta.save()
        #
        SaleDetail.objects.bulk_create(ventas_detalle)
        return Response({'Msj':'Venta registrada correctamente!'})

class RegistrarVenta2(CreateAPIView):
    """ Forma de registrar la venta con el ListField"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    serializer_class = ProcesoVentaSerializer2

    def create(self, request, *args, **kwargs):
        serializer = ProcesoVentaSerializer2(data = request.data)
        #
        serializer.is_valid(raise_exception=True)
        #
        venta = Sale.objects.create(
            date_sale = timezone.now(),
            amount = 0,
            count = 0,
            type_invoce = serializer.validated_data['type_invoce'],
            type_payment = serializer.validated_data['type_payment'],
            adreese_send = serializer.validated_data['adreese_send'],
            user = self.request.user,
        )
        #variables para venta
        amount=0 #monto total de venta
        count=0
        #recuperamos los productos de la venta
        productos = Product.objects.filter(
            #Filtra todos los productos que tienen los ids enviados en el array
            id__in = serializer.validated_data['productos']
        )
        # recuperamos las cantidades enviadas en el array 'cantidades'
        cantidades = serializer.validated_data['cantidades']
        #
        ventas_detalle = []
        #
        for producto, cantidad in zip(productos, cantidades):
            venta_detalle = SaleDetail(
                sale = venta,
                product = producto,
                count = cantidad,
                price_purchase = producto.price_purchase,
                price_sale = producto.price_sale,
            )
            amount = amount + cantidad * producto.price_sale
            count = count + cantidad
            ventas_detalle.append(venta_detalle)
        
        venta.amount = amount
        venta.count = count
        venta.save()
        #
        SaleDetail.objects.bulk_create(ventas_detalle)
        return Response({'Msj':'Venta registrada correctamente!'})
