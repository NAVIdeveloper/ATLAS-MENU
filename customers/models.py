from django.db import models
from partners.models import Partner,Product,Branch,PromoCode,Language,Combo
# Create your models here.

class Customer(models.Model):
    fullname = models.CharField(max_length=50,null=True,blank=True)
    phone = models.CharField(max_length=50,null=True,blank=True)
    telegram_id = models.CharField(max_length=100)
    partner = models.ForeignKey(Partner,on_delete=models.CASCADE)
    language = models.ForeignKey(Language,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.fullname

class Order(models.Model):
    STATUS_CHOICES = [
        ('A', 'Accepted'),
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('X', 'Rejected'),
    ]
    SERVICE_TYPE = [
        ('D', 'Delivery'),
        ('P', 'Pickup'),
    ]
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    service = models.CharField(max_length=1, choices=STATUS_CHOICES)
    
    # Specific fields for delivery
    delivery_address = models.CharField(max_length=255, null=True, blank=True)
    delivery_location_lat = models.CharField(max_length=100,null=True,blank=True)
    delivery_location_long = models.CharField(max_length=100,null=True,blank=True)
    
    # Specific fields for pickup
    pickup_time_avarage = models.CharField(max_length=100,null=True,blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)

    # Promo Code
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    discounted_amount = models.IntegerField(default=0)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    total_amount = models.PositiveIntegerField(default=0)

    message_id = models.CharField(max_length=100,null=True,blank=True)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.fullname} - {self.department.Partner.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    combo = models.ForeignKey(Combo,on_delete=models.SET_NULL,null=True,blank=True)
    # promotion = models.ForeignKey(Promotion,on_delete=models.SET_NULL,null=True,blank=True)

    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.order.customer.fullname}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='cart')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='on_cart')
    # combo = models.ForeignKey(Combo,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=1)

    datetime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.customer.fullname
