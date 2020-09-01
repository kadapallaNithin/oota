from django.contrib import admin
from .models import Product, Rate, ProductIPAddress, ServerKey

admin.site.register(Product)
admin.site.register(Rate)
admin.site.register(ProductIPAddress)
admin.site.register(ServerKey)