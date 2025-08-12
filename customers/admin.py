from django.contrib import admin

# Register your models here.
from customers.models import Customer,Cart,Order,OrderItem

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)