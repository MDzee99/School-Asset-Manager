from django.urls import path 
from . import views 



app_name = "schools"

urlpatterns = [
   path('add/', views.add_school, name='add_school'),
   path('view/', views.view_schools, name='view_schools'),


]