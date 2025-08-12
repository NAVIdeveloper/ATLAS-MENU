from django.db import models
from core.models import User,City,Language
# Create your models here.

class Partner(models.Model):
    name = models.CharField(max_length=120)
    logo = models.FileField(upload_to='partners/')
    phone = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    bot_token = models.CharField(max_length=255)
    primary_color = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Branch(models.Model):
    partner = models.ForeignKey(Partner,on_delete=models.CASCADE)
    
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    location_lat = models.CharField(max_length=100)
    location_long = models.CharField(max_length=100)

    telegram_id = models.CharField(max_length=100)
    group_id = models.CharField(max_length=100,null=True,blank=True)
    
    delivery_enabled = models.BooleanField(default=True)
    pickup_enabled = models.BooleanField(default=True)
    is_open = models.BooleanField(default=False)

    max_distance = models.FloatField(default=1.5)    

    language = models.ForeignKey(Language,on_delete=models.SET_NULL,null=True)
    # message_callback = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return f"{self.partner.name}, {self.city.name}, {self.location}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.FileField(upload_to='products/')
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Combo(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,blank=True)
    image = models.FileField(upload_to='products/combo/')
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

class PromoCode(models.Model):
    partner = models.ForeignKey(Partner,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    
    minimum_order_value = models.BigIntegerField(default=0)
    discount_percentage = models.FloatField(default=0)
    discount_amount = models.FloatField(default=0)

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=False)
 
    def __str__(self):
        return self.code
