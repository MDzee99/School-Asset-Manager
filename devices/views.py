from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
import openpyxl

from devices.models import Device
from schools.models import School
from accounts.models import REGION_CHOICES


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'admin')


@user_passes_test(is_admin)
@login_required
def devices_with_schools_view(request):
    query = request.GET.get('q')
    region = request.GET.get('region')

    devices = Device.objects.select_related('school', 'added_by')

    if query:
        devices = devices.filter(
            Q(school__name__icontains=query) |
            Q(school__school_id__icontains=query) |
            Q(school__city__icontains=query) |
            Q(school__region__icontains=query) |
            Q(added_by__first_name__icontains=query) |
            Q(added_by__last_name__icontains=query) |
            Q(device_type__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(status__icontains=query) |
            Q(operating_system__icontains=query)
        )

    if region:
        devices = devices.filter(school__region=region)
        messages.success(request, "✅ Device updated successfully.")


    return render(request, 'devices/devices_with_schools.html', {
        'devices': devices,
        'regions': REGION_CHOICES,
        'selected_region': region,
        'search_query': query
    })

@login_required
def edit_device_inline_view(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    school = device.school

    if request.method == 'POST':
        # ✅ تحديث بيانات الجهاز
        device.device_type = request.POST['device_type']
        device.serial_number = request.POST['serial_number']
        device.brand = request.POST['brand']
        device.model = request.POST['model']
        device.status = request.POST['status']
        device.operating_system = request.POST['operating_system']
        device.notes = request.POST.get('notes', '')
        device.save()

        # ✅ تحديث بيانات المدرسة
        school.name = request.POST['school_name']
        school.location = request.POST['school_location']
        school.pc_needed = request.POST.get('school_pc') or 0
        school.laptop_needed = request.POST.get('school_laptop') or 0
        school.projector_needed = request.POST.get('school_projector') or 0
        school.labs_count = request.POST.get('school_labs') or 0
        school.classes_count = request.POST.get('school_classes') or 0
        school.save()

        messages.success(request, "✅ Device and School updated successfully.")
        return redirect('devices:devices_with_schools')

    return render(request, 'devices/edit_device.html', {'device': device})



@login_required
def delete_device_view(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    device.delete()
    messages.success(request, "✅ Device deleted successfully.")
    return redirect('devices:devices_with_schools')


@user_passes_test(is_admin)
@login_required
def export_devices_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Devices"

    headers = [
        "Technician", "School", "School ID", "Region", "City",
        "Labs", "Classes", "PCs needed ", "Laptops needed", "Projectors needed",
        "Type Device", "Serial", "Brand", "Model", "Status", "OS", "Note", "Created At"
    ]
    ws.append(headers)

    for d in Device.objects.select_related("school", "added_by"):
        ws.append([
            f"{d.added_by.first_name} {d.added_by.last_name}",
            d.school.name, d.school.school_id, d.school.region, d.school.city,
            d.school.labs_count, d.school.classes_count,
            d.school.pc_needed, d.school.laptop_needed, d.school.projector_needed,
            d.device_type, d.serial_number, d.brand, d.model,
            d.status, d.operating_system, d.notes,
            d.created_at.strftime("%Y-%m-%d %H:%M")
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename=\"devices.xlsx\"'
    wb.save(response)
    return response





