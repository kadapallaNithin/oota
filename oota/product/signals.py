from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductIPAddress, ServerKey
from payments.models import WaterTransaction, Plan
@receiver(post_save,sender=Product)
def create_product_ip_address(sender,instance,created,**kwargs):
    if created:
        ProductIPAddress.objects.create(product=instance,ip="127.0.0.1")
        ServerKey.objects.create(product=instance,key="nithin")
        plan = Plan.objects.create(product=instance,user_id=1,limit=0,used=0)
        WaterTransaction.objects.create(plan=plan,dispensed=0,request=0,key="nithin",not_finished=False)