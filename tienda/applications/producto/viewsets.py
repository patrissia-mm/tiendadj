from rest_framework import viewsets
from rest_framework.response import Response
#
from .models import Colors, Product
from .serializers import (
    ColorsSerializer, 
    ProductSerializer,
    PaginationSerializer,
    ProductSerializerViewSet
)

class ColorViewSet(viewsets.ModelViewSet):
    serializer_class = ColorsSerializer
    queryset = Colors.objects.all()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializerViewSet
    queryset = Product.objects.all()
    pagination_class = PaginationSerializer

    # def create(self, request):
    #     print(request.data)
    #     return Response({"code":"ok"})
    
    def perform_create(self, serializer):
        serializer.save(
            video = "https://www.youtube.com/watch?v=qQkBeOisNM0&list=RDgslVDBS0VeI&index=27"
        )
    
    def list(self, request, *args, **kwargs):
        queryset = Product.objects.productos_por_user(self.request.user)
        #
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


