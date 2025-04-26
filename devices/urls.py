from django.urls import path 
from . import views 

app_name = "devices"

urlpatterns = [
    path('all/', views.devices_with_schools_view, name='devices_with_schools'),  # ← انت كاتبه with_schools لازم يكون نفسه في redirect
    path('edit/<int:device_id>/', views.edit_device_inline_view, name='edit_device'),
    path('delete/<int:device_id>/', views.delete_device_view, name='delete_device'),
    path("export/excel/", views.export_devices_excel, name="export_devices_excel"),

]
