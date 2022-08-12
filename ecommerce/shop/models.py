from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_costumer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Costumer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='costumers/',blank=True,null=True)