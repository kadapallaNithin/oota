from django.db import models
from django.urls import reverse
from home.models import Address
from django.contrib.auth.models import User

class Product(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    address = models.ForeignKey(Address,models.CASCADE,related_name='prod_address')#CharField(max_length=64)
    count_per_unit = models.IntegerField()

    @property
    def details(self):
        return f"{self.name} { self.address.details }"
    def __str__(self):
        return f'{ self.name }'

#should not update foreign key dependency by water_postpaid_transaction model but creation is ok
class Rate(models.Model):
    product =  models.ForeignKey(Product,on_delete=models.CASCADE,parent_link=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    liters_per_unit = models.DecimalField(max_digits=10,decimal_places=3,default=1)
    units = models.CharField(default='Rs/L', max_length=16)
    def __str__(self):
        return f'{ self.amount } { self.units }'
    def get_absolute_url(self):
        return reverse('rates-list')

class ProductIPAddress(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    ip = models.CharField(max_length=16)#GenericIPAddressField()
#    product_key = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now=True)

class ServerKey(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    key = models.CharField(max_length=128,default="nithinPk")
    time = models.DateTimeField(auto_now=True)