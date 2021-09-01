#from _typeshed import Self
from typing import ClassVar
from django.db import models

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit_price = models.CharField(max_length=3,default=1)
    #unit_price = models.DecimalField(decimal_places=2,max_digits=5)

    class Meta:
        #abstract=True
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

def __str__(self):
    return self.name



