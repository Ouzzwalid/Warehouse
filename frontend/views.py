from django.shortcuts import redirect, render 
from user.forms import CreateUserForm


# Create your views here.
def index(request):
    if request.method == 'POST':
        signupForm = CreateUserForm(request.POST)
        if signupForm.is_valid():
            signupForm.save()
            return redirect('index')
    else:
        signupForm = CreateUserForm()

    context = {
        'signupForm': signupForm,
    }
    return render(request, 'frontend/index.html', context)