from django.contrib import admin
from SchoolAssetManager.accounts.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'region', 'city',
        'employee_id', 'phone', 'email', 'role'
    )
    list_filter = ('region', 'city', 'role')
    search_fields = ('username', 'first_name', 'last_name', 'employee_id', 'phone', 'email')

# فقط سجل المستخدم إذا ما كان مسجل قبل
try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass




