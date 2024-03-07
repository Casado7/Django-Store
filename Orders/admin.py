from django.contrib import admin

from Orders.models import Order, Order_Line

# Register your models here.
admin.site.register([Order,Order_Line])