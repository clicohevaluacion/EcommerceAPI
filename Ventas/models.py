from django.db import models

import uuid
from django.contrib.auth.models import User


# Create your models here.


class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True, blank=False)
    # id =    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name =  models.CharField(db_column='sName', max_length=100, blank=True, null=True, unique=True)
    price = models.FloatField(db_column='fPrice', blank=False, null=False, default=0)
    stock = models.IntegerField(db_column='iStock', blank=False, null=False, default=0)

    class Meta:
        db_table = 'Product'
        verbose_name_plural = 'Products'
        verbose_name = 'Product'

    def __str__(self):
        return str(self.id)

class Order(models.Model):
    id =        models.IntegerField(db_column='id', primary_key=True, blank=False, null=False, unique=True)
    date_time = models.DateTimeField(db_column='fDatetime', null=True, blank=True, auto_now_add=True)

    class Meta:
        db_table = 'Order'
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.id is None:
            try:
                self.id = Order.objects.all().order_by('id').last().id + 1
            except:
                self.id = 1
        super(Order, self).save(*args, **kwargs)

class OrderDetail(models.Model):
    order =    models.ForeignKey('Order', models.SET_NULL, blank=False, null=True)
    cuantity = models.IntegerField(db_column='iCuantity', blank=False, null=False, default=0)
    product =  models.ForeignKey('Product', models.SET_NULL, blank=False, null=True)

    class Meta:
        db_table = 'OrderDetail'
        verbose_name_plural = 'OrdersDetails'
        verbose_name = 'OrderDetail'

    def __str__(self):
        return str(self.order)




















