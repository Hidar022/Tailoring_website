from django.contrib import admin
from .models import Product, Order, Measurement

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Measurement)
