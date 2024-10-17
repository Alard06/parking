from django.contrib import admin

from main.models import *

class ParkingAdmin(admin.ModelAdmin):
    pass


class ModelAdmin(admin.ModelAdmin):
    pass

class ManufactureAdmin(admin.ModelAdmin):
    pass


admin.site.register(Parking, ParkingAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Manufacture, ManufactureAdmin)