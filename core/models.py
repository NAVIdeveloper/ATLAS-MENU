from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    is_partner = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class City(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class EngineBotText(models.Model):
    language = models.OneToOneField(Language,on_delete=models.SET_NULL,null=True,related_name='customer_text')
    info = models.TextField(null=True,blank=True)    
    start = models.TextField(null=True,blank=True)
    ask_phone = models.TextField(null=True,blank=True)
    success_phone = models.TextField(null=True,blank=True)
    main_menu = models.TextField(null=True,blank=True)
    no_orders = models.TextField(null=True,blank=True)
    empty_cart = models.TextField(null=True,blank=True)
    cart_info = models.TextField(null=True,blank=True)
    ask_city = models.TextField(null=True,blank=True)
    ask_department = models.TextField(null=True,blank=True)
    ask_service_type = models.TextField(null=True,blank=True)
    ask_delivery_location = models.TextField(null=True,blank=True)
    error_many_department = models.TextField(null=True,blank=True)
    error_distance = models.TextField(null=True,blank=True)
    ask_takeaway_time = models.TextField(null=True,blank=True)
    info_distance = models.TextField(null=True,blank=True)    
    ask_comment = models.TextField(null=True,blank=True)
    ask_inform = models.TextField(null=True,blank=True)
    order_informed = models.TextField(null=True,blank=True)
    order_canceled = models.TextField(null=True,blank=True)
    order_info = models.TextField(null=True,blank=True)
    order_info_takeaway = models.TextField(null=True,blank=True)
    order_status = models.TextField(null=True,blank=True)
    
    btn_menu = models.CharField(max_length=100,null=True,blank=True)
    btn_orders = models.CharField(max_length=100,null=True,blank=True)
    btn_cart = models.CharField(max_length=100,null=True,blank=True)
    btn_message = models.CharField(max_length=100,null=True,blank=True)
    btn_ask_phone = models.CharField(max_length=100,null=True,blank=True)
    btn_settings = models.CharField(max_length=100,null=True,blank=True)
    btn_back = models.CharField(max_length=100,null=True,blank=True)
    btn_clear = models.CharField(max_length=100,null=True,blank=True)
    btn_comfirm = models.CharField(max_length=100,null=True,blank=True)
    btn_location = models.CharField(max_length=100,null=True,blank=True)
    btn_no = models.CharField(max_length=100,null=True,blank=True)
    btn_yes = models.CharField(max_length=100,null=True,blank=True)
    btn_complete = models.CharField(max_length=100,null=True,blank=True)
    btn_accept = models.CharField(max_length=100,null=True,blank=True)
    btn_return = models.CharField(max_length=100,null=True,blank=True)
    
    label_main_menu = models.CharField(max_length=100,null=True,blank=True)
    label_open = models.CharField(max_length=100,null=True,blank=True)
    label_close = models.CharField(max_length=100,null=True,blank=True)
    label_cart_cleared = models.CharField(max_length=100,null=True,blank=True)
    label_cart_item = models.CharField(max_length=100,null=True,blank=True)
    label_minute = models.CharField(max_length=100,null=True,blank=True)

    label_pending = models.CharField(max_length=100,null=True,blank=True)
    label_completed = models.CharField(max_length=100,null=True,blank=True)
    label_accepted = models.CharField(max_length=100,null=True,blank=True)
    label_rejected = models.CharField(max_length=100,null=True,blank=True)
 
    def __str__(self):
        return self.language

class MasterBotText(models.Model):
    language = models.OneToOneField(Language,on_delete=models.SET_NULL,null=True,related_name='master')
    command_start = models.TextField(null=True,blank=True)
    has_group = models.TextField(null=True,blank=True)
    has_no_group = models.TextField(null=True,blank=True)
    new_group_confirmed = models.TextField(null=True,blank=True)

    group_confirmed = models.TextField(null=True,blank=True)

    btn_settings = models.CharField(max_length=100,null=True,blank=True)
    btn_statistic = models.CharField(max_length=100,null=True,blank=True)
    btn_add_group = models.CharField(max_length=100,null=True,blank=True)
    btn_dashboard = models.CharField(max_length=100,null=True,blank=True)

    btn_settings_language = models.CharField(max_length=100,null=True,blank=True)
    btn_setting_group = models.CharField(max_length=100,null=True,blank=True)
    btn_settings_door_state = models.CharField(max_length=100,null=True,blank=True)
    btn_settings_orders_state = models.CharField(max_length=100,null=True,blank=True)
 
    def __str__(self):
        return self.language.name