from django.urls import path
from customers.views import render_close_webapp_page

urlpatterns = [
    path('close-webapp/',render_close_webapp_page,name='close_webapp')
]