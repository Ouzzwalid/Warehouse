from unicodedata import name
from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from .forms import CreateUserForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 2
            user.save()
    else:        
        form = CreateUserForm()
    return render(request, 'user/register.html',{'form': form})
