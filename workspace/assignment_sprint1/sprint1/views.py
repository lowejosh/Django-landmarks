from django.shortcuts import render, redirect
from django.http import HttpResponse
# Signup imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from sprint1.forms import SignUpForm

# Index page view
def index(request):
    # If the user is logged in
    if (request.user.is_authenticated()):
        # Define the navbar to only show logout button
        navBar = '<h5><a href="/logout/">Log out</a><br />'
    # If the user isn't logged in
    else:
        # Define the navbar to show login button
        navBar = '<h5><a href="/login/">Log in</a><br /><a href="/signup/">Register</a></h5>'

    # Define the context of the python vars
    context_dict = {'navBar' : navBar,}

    # Return the template
    return render(request, 'publicMain.html', context=context_dict)

# Signup page view
def signup(request):

    # Define the navbar
    navBar = '<h5><a href="/login/">Log in</a><br /><a href="/signup/">Register</a></h5>'

    # Form functions
    if request.method == 'POST' :
        form = SignUpForm(request.POST)
        if form.is_valid():

            # Retrieve data from forms and link to the User model
            user = form.save()
            user.refresh_from_db()  # Loads the profile instance created from the signal
            user.profile.firstName = form.cleaned_data.get('firstName')
            user.profile.lastName = form.cleaned_data.get('lastName')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.accountType = form.cleaned_data.get('accountType')
            user.profile.dateOfBirth = form.cleaned_data.get('dateOfBirth')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phoneNumber = form.cleaned_data.get('phoneNumber')
            user.profile.address = form.cleaned_data.get('address')
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # Create, login and redirect to index page
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    # Render the page and set the context of python variables
    return render(request, 'signup.html', {'form': form, 'navBar' : navBar,})

# Location Index
def locations(request, location_id):
    # If the user is logged in
    if (request.user.is_authenticated()):
        # Define the navbar to only show logout button
        navBar = '<h5><a href="/logout/">Log out</a><br />'
    # If the user isn't logged in
    else:
        # Define the navbar to show login button
        navBar = '<h5><a href="/login/">Log in</a><br /><a href="/signup/">Register</a></h5>'

    # Define the context of the python vars
    context_dict = {'navBar' : navBar, 'location_id' : location_id,}

    # Return the template
    return render(request, 'locations.html', context=context_dict)
    
