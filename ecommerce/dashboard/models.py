from django.db import models
from django import forms
from django.db.models.deletion import CASCADE
from shop.models import *
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()

    def __str__(self):
          return self.name
          
class Product(models.Model):
      name=models.CharField(max_length=100)
      description=models.TextField()
      brand=models.CharField(max_length=100)
      price=models.FloatField()
      countInStock=models.IntegerField()
      image=models.ImageField(upload_to = "products/")
      category=models.ForeignKey(Category,on_delete=models.CASCADE)

      def __str__(self):
          return self.name

class Creditcard(models.Model):
    type=models.CharField(max_length=50)
    numero_carte=models.BigIntegerField()
    date_exp=models.DateField()
    CVV=models.IntegerField()
    costumer=models.ForeignKey(Costumer,on_delete=models.CASCADE)


class Order(models.Model):
    costumer=models.ForeignKey(Costumer,on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

class AdminUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='admins/',blank=True)


