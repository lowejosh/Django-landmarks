from django.shortcuts import render, redirect
from django.http import HttpResponse
# Signup imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from sprint1.forms import SignUpForm

# Index page view
def index(request):
    # Define the context of the python vars
    context_dict = { }
    # Return the template
    return render(request, 'publicMain.html', context=context_dict)

# --OLD--  Register page view
def register(request):
    # Define the context of the python vars
    context_dict = {'navBar': '<h5><a>Log in</a><br /><a>Register</a></h5>', }
    # Return the template
    return render(request, 'base.html', context=context_dict)

# --NEW-- Signup page view
def signup(request):

    # Define the navbar
    navBar = '<h5><a>Log in</a><br /><a>Register</a></h5>'

    # Form functions
    if request.method == 'POST' :
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'navBar' : navBar,})


