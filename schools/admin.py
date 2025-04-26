from django.contrib import admin
from SchoolAssetManager.schools.models import School

class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'school_id', 'region', 'city', 'labs_count', 'classes_count',
        'pc_needed', 'laptop_needed', 'projector_needed', 'added_by_name', 'created_at'
    )
    list_filter = ('region', 'city')
    search_fields = ('name', 'school_id', 'region', 'city', 'added_by__first_name', 'added_by__last_name')
    readonly_fields = ['created_at']

    def added_by_name(self, obj):
        return f"{obj.added_by.first_name} {obj.added_by.last_name}" if obj.added_by else "-"

try:
    admin.site.unregister(School)
except admin.sites.NotRegistered:
    pass


admin.site.register(School, SchoolAdmin)

