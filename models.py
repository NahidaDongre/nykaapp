from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    CAT=(1,"Makeup"),(2,"SkinCare"),(3,"HairCare"),(4,"Fragrances"),
    pname=models.CharField(max_length=50, verbose_name="Product Name")
    price=models.FloatField()
    category=models.IntegerField(choices=CAT, verbose_name="Category")
    description=models.CharField(max_length=300, verbose_name="Details")
    is_active=models.BooleanField(default=True, verbose_name="Is_Available")
    pimage=models.ImageField(upload_to='image')

    def __str__(self):
        return self.pname


class Cart(models.Model):
    userid=models.ForeignKey('auth.user',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Brand(models.Model):
    CAT=(
        (1,"Nykaa"),
        (2,"LAKME"),
        (3,"LOREAL PARIS"),
        (4,"MAYBELLINE"),
        (5,"Mac"),
    )
    bname=models.CharField(max_length=50, verbose_name="Brand Name")
    price=models.FloatField()
    category=models.IntegerField(choices=CAT, verbose_name="Category")
    description=models.CharField(max_length=300, verbose_name="Details")
    is_active=models.BooleanField(default=True, verbose_name="Is_Available")
    pimage=models.ImageField(upload_to='image')
    def __str__(self):
        return self.name


class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey('auth.user',on_delete=models.CASCADE, db_column='user_id')
    p_id=models.ForeignKey('Product',on_delete=models.CASCADE,db_column="p_id")
    qty=models.IntegerField(default=1)
    amt=models.FloatField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    def __str__(self):
        return self.user.username