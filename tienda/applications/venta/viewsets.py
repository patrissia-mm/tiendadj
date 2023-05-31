from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
#
from django.utils import timezone
from django.shortcuts import get_object_or_404
#
from applications.producto.models import Product
#
from .serializers import ProcesoVentaSerializer2, VentaReporteSerializers
#
from .models import Sale, SaleDetail

class VentasViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]
    # serializer_class = VentaReporteSerializers
    queryset = Sale.objects.all()

    def get_permissions(self):
        if (self.action =='list' or self.action == "retrieve"):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = Sale.objects.all()
        serializer = VentaReporteSerializers(queryset, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = ProcesoVentaSerializer2(data = request.data)
        serializer.is_valid(raise_exception = True)
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

    
    def retrieve(self, request, pk=None):
        # venta = Sale.objects.get(id=pk)
        venta = get_object_or_404(Sale.objects.all(), id=pk)
        serializer = VentaReporteSerializers(venta)
        return Response(serializer.data)