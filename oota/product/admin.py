from django.contrib import admin
from .models import Product, Rate, ProductIPAddress

admin.site.register(Product)
admin.site.register(Rate)
admin.site.register(ProductIPAddress)