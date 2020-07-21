from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Address)
admin.site.register(models.Village)
admin.site.register(models.Town)
admin.site.register(models.State)
admin.site.register(models.Country)
