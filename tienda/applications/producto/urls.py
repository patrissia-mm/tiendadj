#django
from django.urls import include, re_path, path
#local
from . import views

app_name = "producto_app"
urlpatterns = [
    path(
        'api/product/por-usuario/',
        views.ListProductUser.as_view(),
        name = 'product-producto_by_user'
    ),
    path(
        'api/product/con-stok/',
        views.ListProductoStok.as_view(),
        name = 'product-producto_con_stok'
    ),
    path(
        'api/product/por-genero/<gender>/',
        views.ListProductoGenero.as_view(),
        name = 'product-producto_por_genero'
    ),
    path(
        'api/product/filtrar/',
        views.FiltrarProductos.as_view(),
        name = 'product-filtrar'
    ),
]