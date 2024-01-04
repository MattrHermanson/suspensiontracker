from django.contrib import admin
from .models import Bike, Setup, Variation, Fork_Setting, Shock_Setting

admin.site.register(Bike)
admin.site.register(Setup)
admin.site.register(Variation)
admin.site.register(Fork_Setting)
admin.site.register(Shock_Setting)