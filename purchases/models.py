from django.db import models
from django.utils.crypto import get_random_string


def _create_key():
    return get_random_string(64).lower()


class ProductPurchase(models.Model):
    '''
    Through model for charges and products.
    '''
    charge = models.ForeignKey('djstripe.Charge', null=True, blank=True)
    product = models.ForeignKey('Product')
    key = models.CharField(max_length=64, unique=True, default=_create_key)
    downloads = models.IntegerField(default=10)

    def decrement_downloads(self):
        self.downloads -= 1
        return self.save()


class Product(models.Model):
    '''
    Purchaseable product
    '''
    name = models.CharField(max_length=500)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    resource = models.FileField(blank=True, null=True)
    downloads = models.IntegerField(default=10)
