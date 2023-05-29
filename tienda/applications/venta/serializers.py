from rest_framework import serializers
#
from .models import Sale, SaleDetail

class VentaReporteSerializers(serializers.ModelSerializer):
    
    producto = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = (
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'adreese_send',
            'user',
            'producto',
        )
    
    def get_producto(self, obj):
        query = SaleDetail.objects.productos_por_venta(obj.id)
        productos_serializados = DetalleVentaProductoSerializer(query, many = True).data
        return  productos_serializados

class DetalleVentaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = (
            'id',
            'sale',
            'product',
            'count',
            'price_purchase',
            'price_sale',
        )

class ProductDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    count = serializers.IntegerField()

class ProcesoVentaSerializer(serializers.Serializer):
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ProductDetailSerializer(many = True)

# Nuevo serializer para registrar venta enviando un array de productos
class ArrayIntegerSerializer(serializers.ListField):
    """ Especificar el tipo de Array"""
    child = serializers.IntegerField()
#
class ProcesoVentaSerializer2(serializers.Serializer):
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ArrayIntegerSerializer()
    cantidades = ArrayIntegerSerializer() 








