from django.contrib import admin

# Register your models here.
from partners.models import (
    Partner,Product,Category,Branch,PromoCode
)
admin.site.register(Partner)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Branch)
admin.site.register(PromoCode)