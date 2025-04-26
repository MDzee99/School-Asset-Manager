from django.contrib import admin
from devices.models import Device  # ✅ Correct import

class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'device_type', 'serial_number', 'brand', 'model', 'status', 'operating_system',
        'school_name', 'school_region', 'school_city', 'added_by_name', 'created_at'
    )
    list_filter = ('school__region', 'device_type', 'status', 'operating_system')
    search_fields = (
        'device_type', 'serial_number', 'brand', 'model', 'status', 'operating_system',
        'school__name', 'school__region', 'school__city', 'added_by__first_name', 'added_by__last_name'
    )
    readonly_fields = ['created_at']

    def school_name(self, obj):
        return obj.school.name if obj.school else '-'

    def school_region(self, obj):
        return obj.school.region if obj.school else '-'

    def school_city(self, obj):
        return obj.school.city if obj.school else '-'

    def added_by_name(self, obj):
        return f"{obj.added_by.first_name} {obj.added_by.last_name}" if obj.added_by else "-"

admin.site.register(Device, DeviceAdmin)
