from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','email','phone')

class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email','phone')

class CreateStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'role', 'phone' )