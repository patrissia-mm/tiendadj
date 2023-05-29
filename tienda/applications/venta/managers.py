from django.db import models

class SaleDetailManager(models.Manager):

    def productos_por_venta(self, venta_id):
        consulta = self.filter(
            sale__id = venta_id
        ).order_by('count', 'product__name')
        return consulta