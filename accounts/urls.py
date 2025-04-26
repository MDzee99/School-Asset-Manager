from django.urls import path 
from . import views 

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_user_view, name='register_user_view'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard-technician/', views.dashboard_technician, name='dashboard_technician'),
    path('add-new-school/', views.add_new_school, name='add_new_school'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('view-users/', views.view_users, name='view_users'),
    path('users/<int:user_id>/edit/', views.update_user_view, name='update_user'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
    path('technician/schools-devices/', views.technician_schools_and_devices, name='technician_schools_devices'),
    # ... باقي المسارات
    path('edit-school/<int:school_id>/', views.edit_school_view, name='edit_school'),
    path('add-device/<int:school_id>/', views.add_device_to_school_view, name='add_device_to_school'),
    
    






]
