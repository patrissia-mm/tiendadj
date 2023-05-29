from rest_framework.generics import (
    ListAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
#
from django.shortcuts import render
#
from .models import Product
from .serializers import ProductSerializer

class ListProductUser(ListAPIView):
    serializer_class = ProductSerializer
    #Mediante el paquete authToken identifica o autentica al usuario
    authentication_classes = (TokenAuthentication,)
    #Síno se identifica al usuario o no se recibe un token, enciar un mensaje
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("*******")
        usuario = self.request.user
        print(usuario)
        return Product.objects.productos_por_user(usuario)

class ListProductoStok(ListAPIView):
    """ Pruebas de diferencia entre authentication_classes y permission_classes"""
    serializer_class = ProductSerializer
    #authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Product.objects.productos_con_stok()
    
class ListProductoGenero(ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        genero = self.kwargs['gender']
        return Product.objects.productos_por_genero(genero)
    
class FiltrarProductos(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        mujer = self.request.query_params.get('man', None)
        varon = self.request.query_params.get('woman', None) 
        nombre = self.request.query_params.get('name', None)
        #
        return Product.objects.filtrar_productos(
            man = varon,
            woman = mujer,
            name = nombre
        )

