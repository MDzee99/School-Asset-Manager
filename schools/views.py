from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def add_school(request):
    return render(request, 'schools/add_school.html')  

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from schools.models import School
from accounts.models import REGION_CHOICES

@login_required
def view_schools(request):
    if not request.user.is_superuser and request.user.role != 'admin':
        return render(request, 'errors/no_permission.html')

    schools = School.objects.select_related('added_by').all()

    region = request.GET.get('region')
    city = request.GET.get('city')
    technician = request.GET.get('technician')

    if region:
        schools = schools.filter(region=region)
    if city:
        schools = schools.filter(city__icontains=city)
    if technician:
        schools = schools.filter(added_by__first_name__icontains=technician)

    return render(request, 'schools/view_schools.html', {
        'schools': schools,
        'regions': REGION_CHOICES,
        'selected_region': region,
        'city': city,
        'technician': technician,
    })
