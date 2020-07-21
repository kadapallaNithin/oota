from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductIPAddress

@receiver(post_save,sender=Product)
def create_product_ip_address(sender,instance,created,**kwargs):
    if created:
        ProductIPAddress.objects.create(product=instance,ip="127.0.0.1",server_key="nithin",product_key="nithin")
        ProductIPAddress.objects.create(product=instance,ip="127.0.0.1",server_key="nithin",product_key="nithin")