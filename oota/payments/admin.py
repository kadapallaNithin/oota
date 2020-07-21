from django.contrib import admin
from .models import Plan, PostPaid, WaterPostPaidTransaction, WaterDispensedPeriodic#, WaterDispensedFinish
admin.site.register(Plan)
admin.site.register(PostPaid)
admin.site.register(WaterPostPaidTransaction)
admin.site.register(WaterDispensedPeriodic)
#admin.site.register(WaterDispensedFinish)