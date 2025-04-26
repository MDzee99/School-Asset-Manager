from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .models import User
from devices.models import Device
from schools.models import School

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin' or request.user.is_superuser:
            return redirect('accounts:dashboard_admin')
        else:
            return redirect('main:home_page')  # ✅ المستخدم العادي يروح للهوم

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'admin' or user.is_superuser:
                return redirect('accounts:dashboard_admin')
            else:
                return redirect('main:home_page')  # ✅ برضو هنا بعد تسجيل الدخول
        else:
            messages.error(request, "❌ Invalid username or password.")

    return render(request, 'accounts/login.html')



def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)

from accounts.models import User, REGION_CHOICES  
@user_passes_test(is_admin)
def register_user_view(request: HttpRequest):
    msg = None
    preserved_data = {}

    if request.method == "POST":
        try:
            username = request.POST["username"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            employee_id = request.POST["employee_id"]
            region = request.POST["region"]
            city = request.POST["city"]
            role = request.POST["role"]
            password = request.POST["password"]
            profile_image = request.FILES.get("profile_image")

            preserved_data = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "employee_id": employee_id,
                "region": region,
                "city": city,
                "role": role,
            }

            if not email.endswith("@tetco.sa"):
                msg = "❌ الإيميل يجب أن ينتهي بـ @tetco.sa"
                raise Exception("Invalid Email Domain")

            if User.objects.filter(Q(username=username) | Q(employee_id=employee_id)).exists():
                msg = "❌ اسم المستخدم أو رقم الموظف مسجل من قبل."
                raise Exception("Duplicate Entry")

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                phone=phone,
                employee_id=employee_id,
                region=region,
                city=city,
                role=role,
                profile_image=profile_image
            )
            user.save()

            messages.success(request, "✅ تم إضافة المستخدم بنجاح!")
            return redirect("accounts:view_users")

        except IntegrityError:
            msg = "⚠️ خطأ في قاعدة البيانات. ربما يوجد تكرار أو مشكلة في الحقول."
        except Exception as e:
            if msg is None:
                msg = f"⚠️ حدث خطأ غير متوقع: {e}"

    return render(request, "accounts/register.html", {
        "msg": msg,
        "regions": REGION_CHOICES,
        "preserved_data": preserved_data
    })



@login_required
def dashboard_admin(request):
    return render(request, "accounts/dashboard_admin.html")


@login_required
def dashboard_technician(request):
    if request.user.role != 'technician':
        return render(request, 'errors/no_permission.html')

    msg = None
    school = None
    form_type = request.POST.get('form_type') if request.method == "POST" else None

    if form_type == 'school':
        try:
            name = request.POST['name']
            school_id = request.POST['school_id']
            location = request.POST['location']
            labs = int(request.POST.get('labs_count') or 0)
            classes = int(request.POST.get('classes_count') or 0)
            pc = int(request.POST.get('pc_needed') or 0)
            laptop = int(request.POST.get('laptop_needed') or 0)
            projector = int(request.POST.get('projector_needed') or 0)
            region = request.user.region
            city = request.user.city
            latitude = float(request.POST.get('latitude') or 0)
            longitude = float(request.POST.get('longitude') or 0)
            image = request.FILES.get('image')

            if School.objects.filter(school_id=school_id).exists():
                messages.error(request, "❌ This school already exists.")
            else:
                school = School.objects.create(
                    name=name,
                    school_id=school_id,
                    location=location,
                    labs_count=labs,
                    classes_count=classes,
                    pc_needed=pc,
                    laptop_needed=laptop,
                    projector_needed=projector,
                    image=image,
                    added_by=request.user,
                    region=region,
                    city=city,
                    latitude=latitude,
                    longitude=longitude,
                )
                request.session['school_id'] = school.id
                messages.success(request, "✅ School added successfully!")
                return redirect('accounts:dashboard_technician')
        except Exception as e:
            messages.error(request, f"⚠️ Error while adding school: {str(e)}")

    elif form_type == 'device':
        try:
            school_id = request.session.get('school_id')
            if not school_id:
                messages.error(request, "⚠️ No school selected.")
            else:
                school = School.objects.get(id=school_id)
                Device.objects.create(
                    school=school,
                    device_type=request.POST['device_type'],
                    serial_number=request.POST['serial_number'],
                    brand=request.POST['brand'],
                    model=request.POST['model'],
                    status=request.POST['status'],
                    operating_system=request.POST['operating_system'],
                    notes=request.POST.get('notes', ''),
                    added_by=request.user
                )
                msg = "✅ Device added successfully!"
        except Exception as e:
            msg = f"⚠️ Error while adding device: {str(e)}"

    school_id = request.session.get('school_id')
    if school_id:
        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            school = None

    return render(request, 'accounts/dashboard_technician.html', {'school': school, 'msg': msg})




@login_required
def technician_schools_and_devices(request):
    if request.user.role != 'technician':
        return render(request, 'errors/no_permission.html')

    query = request.GET.get('q')
    schools = School.objects.filter(added_by=request.user).prefetch_related('devices')

    if query:
        schools = schools.filter(
            Q(name__icontains=query) |
            Q(school_id__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query)
        )

    return render(request, 'accounts/technician_schools_devices.html', {
        'schools': schools,
        'search_query': query,
    })



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from schools.models import School
from devices.models import Device

@login_required
def edit_school_view(request, school_id):
    school = get_object_or_404(School, id=school_id, added_by=request.user)
    
    if request.method == 'POST':
        school.name = request.POST['name']
        school.school_id = request.POST['school_id']
        school.location = request.POST['location']
        school.labs_count = int(request.POST.get('labs_count') or 0)
        school.classes_count = int(request.POST.get('classes_count') or 0)
        school.pc_needed = int(request.POST.get('pc_needed') or 0)
        school.laptop_needed = int(request.POST.get('laptop_needed') or 0)
        school.projector_needed = int(request.POST.get('projector_needed') or 0)
  
        if request.FILES.get('image'):
            school.image = request.FILES.get('image')
        school.save()
        messages.success(request, "✅ School updated successfully.")
        return redirect('accounts:technician_schools_devices')  # غيّريها حسب اسم صفحة عرض المدارس

    return render(request, 'accounts/edit_school.html', {'school': school})




@login_required
def add_device_to_school_view(request, school_id):
    school = get_object_or_404(School, id=school_id, added_by=request.user)

    if request.method == 'POST':
        Device.objects.create(
            school=school,
            device_type=request.POST['device_type'],
            serial_number=request.POST['serial_number'],
            brand=request.POST['brand'],
            model=request.POST['model'],
            status=request.POST['status'],
            operating_system=request.POST['operating_system'],
            notes=request.POST.get('notes', ''),
            added_by=request.user
        )
        messages.success(request, "✅ Device added successfully!")
        return redirect('accounts:technician_schools_devices')

    return render(request, 'accounts/add_device_to_school.html', {'school': school})



@login_required
def add_new_school(request):
    if request.user.role != 'technician':
        return render(request, 'errors/no_permission.html')

    if 'school_id' in request.session:
        del request.session['school_id']  # يحذف الربط بس من الجلسة، مو من الداتابيس

    return redirect('accounts:dashboard_technician')


@requires_csrf_token
def custom_csrf_failure_view(request, reason=""):
    return render(request, "accounts/login.html", {
        "msg": "⚠️ Session expired or invalid token. Please refresh the page and try again."
    }, status=200)


def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            if request.user.role == 'admin' or request.user.is_superuser:
                return redirect('accounts:dashboard_admin')
            else:
                return redirect('accounts:dashboard_technician')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})



from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from accounts.forms import CustomUserUpdateForm
from accounts.models import REGION_CHOICES

@login_required
def view_users(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return render(request, 'errors/no_permission.html')

    users = User.objects.all().order_by('-date_joined')

    # هنا نحدد صلاحية التعديل
    can_edit_users = request.user.is_superuser or request.user.has_perm('accounts.can_edit_users')

    query = request.GET.get('q')
    region = request.GET.get('region')

    if query:
        users = users.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(phone__icontains=query) |
            Q(city__icontains=query) |
            Q(region__icontains=query)
        )

    if region:
        users = users.filter(region=region)

    return render(request, 'accounts/view_users.html', {
        'users': users,
        'regions': REGION_CHOICES,
        'can_edit_users': can_edit_users  # ✅ هذا هو المهم
    })



from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.forms import CustomUserUpdateForm

User = get_user_model()

@login_required
def update_user_view(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    if not request.user.is_superuser and not request.user.has_perm('accounts.can_edit_users'):
        messages.error(request, "❌ You do not have permission.")
        return redirect('accounts:view_users')

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if email and not email.endswith('@tetco.sa'):
                messages.error(request, "❌ الإيميل يجب أن ينتهي بـ @tetco.sa")
                return redirect('accounts:update_user', user_id=user_id)

            if user_obj == request.user and form.cleaned_data['role'] != 'admin':
                messages.error(request, "❌ You cannot change your own role.")
                return redirect('accounts:update_user', user_id=user_id)

            form.save()

            new_password = request.POST.get('new_password')
            if new_password:
                user_obj.set_password(new_password)
                user_obj.save()

            messages.success(request, "✅ User updated successfully.")
            return redirect('accounts:view_users')
    else:
        form = CustomUserUpdateForm(instance=user_obj)

    return render(request, 'accounts/update_user.html', {
        'form': form,
        'user_obj': user_obj
    })


from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()

@login_required
def delete_user_view(request, user_id):
    if not request.user.is_superuser and not request.user.has_perm('accounts.delete_user'):
        messages.error(request, "❌ You do not have permission to delete users.")
        return redirect('accounts:view_users')

    user_obj = get_object_or_404(User, id=user_id)

    if user_obj == request.user:
        messages.error(request, "❌ You cannot delete your own account.")
        return redirect('accounts:view_users')

    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, "✅ User deleted successfully.")
        return redirect('accounts:view_users')

    return render(request, 'accounts/confirm_delete_user.html', {
        'user_obj': user_obj
    })


