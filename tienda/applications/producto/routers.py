from rest_framework.routers import DefaultRouter
#
from . import viewsets

router = DefaultRouter()

router.register(r'colors', viewsets.ColorViewSet, basename = 'colors')
router.register(r'products', viewsets.ProductViewSet, basename = 'products')

urlpatterns = router.urls