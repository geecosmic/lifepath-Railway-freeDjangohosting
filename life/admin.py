from django.contrib import admin


# Register your models here.
from . models import Period,YearlyPeriod

admin.site.register(Period)
admin.site.register(YearlyPeriod)
