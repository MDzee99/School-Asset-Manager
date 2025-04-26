from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='اسم المستخدم', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='كلمة المرور')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'employee_id', 'region', 'city', 'profile_image', 'password']


from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'employee_id', 'phone', 'region', 'city', 'role', 'profile_image']

