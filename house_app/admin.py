from django.contrib import admin
from .models import House, Resident, MaintenanceRequest


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        'address', 'city', 'state', 'zip_code', 'is_available', 'rent', 'num_bedrooms', 'num_bathrooms'
    )
    search_fields = ('address', 'city', 'state', 'zip_code')


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'house', 'email', 'phone', 'move_in_date', 'move_out_date')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('house',)


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'house', 'resident', 'status', 'category', 'created_at', 'updated_at')
    list_filter = ('status', 'category', 'house')
    search_fields = ('title', 'description', 'resident__first_name', 'resident__last_name')
from django.contrib import admin

# Register your models here.
