from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from sprint1.models import Location
# Signup imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from sprint1.forms import SignUpForm, EditProfileForm, EmailForm, DeleteUserForm, ContactForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

# Navbar function that returns the proper list 
def navBarFunc(isLogged): 
    if (isLogged == True):
        return '<ul><li><a href="/">Home</a></li><li class="right"><a href="/logout/">Log out</a></li><li><a href="/location/page-1">Locations</a></li><li class="right"><a href="/modify/">Modify Account</a></li></ul>'
    else:
        return '<ul><li><a href="/">Home</a></li><li class="right"><a href="/login/">Log in</a></li><li class="right"><a href="/signup/">Register</a></li><li><a href="/location/page-1">Locations</a></li></ul>'

# Function that returns the html output of a location
def locationOutput(locationId):
    try:
        l = Location.objects.get(id=locationId)
    except: 
        return ""

    locationName = l.locationName
    locationBio = l.locationBio
    locationSt = l.locationAddress
    linkId = str(locationId)

    return """
        <div class='location-wrap'>
            <a class="location-name" href="/location/individual/""" + linkId + """">""" + locationName + """</a>
            <span class='location-bio'>""" + locationSt + """</span>
        </div>
    """



# Index page view
def index(request):
    # If the user is logged in
    if (request.user.is_authenticated()):
        # Define the navbar to only show logout button
        navBar = navBarFunc(True)   
        # Define the context of the python vars
        context_dict = {'navBar' : navBar,}
        # Return the template
        return render(request, 'privateMain.html', context=context_dict)
        # If the user isn't logged in
    else:
        # Define the navbar to show login button
        navBar = navBarFunc(False) 
        # Define the context of the python vars
        context_dict = {'navBar' : navBar,}
        # Return the template
        return render(request, 'publicMain.html', context=context_dict)
        

# Signup page view
def signup(request):

    # Define the navbar
    navBar = navBarFunc(False)

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
# needs a lot of work
def locations(request, location_id):
    # Show the correct navBar
    if (request.user.is_authenticated()):
        navBar = navBarFunc(True)
    else:
        navBar = navBarFunc(False)

    # Define the context of the python vars
    context_dict = {'navBar' : navBar, 'location_id' : location_id,}

    # Return the template
    return render(request, 'viewLocation.html', context=context_dict)

    
# Location Feed
def locationfeed(request, page):

    # To normalize it (yeah i know)
    page = int(page) - 1

    # Show the correct navBar
    if (request.user.is_authenticated()):
        navBar = navBarFunc(True)
    else:
        navBar = navBarFunc(False)

    location1 = locationOutput(page * 8 + 1)
    location2 = locationOutput(page * 8 + 2)
    location3 = locationOutput(page * 8 + 3)
    location4 = locationOutput(page * 8 + 4)
    location5 = locationOutput(page * 8 + 5)
    location6 = locationOutput(page * 8 + 6)
    location7 = locationOutput(page * 8 + 7)
    location8 = locationOutput(page * 8 + 8)

    # Define the context of the python vars
    context_dict = {'navBar' : navBar, 'page': page + 1, 'location1': location1, 'location2': location2, 'location3': location3,'location4': location4,'location5': location5,'location6': location6,'location7': location7,'location8': location8,}

    # Return the template
    return render(request, 'locationfeed.html', context=context_dict)

def modify(request):
    # User must be logged in to access modify page
    navBar = navBarFunc(True)
	
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'navBar' : navBar}
	
    return render(request, 'modify.html', context=context_dict)


def edit_profile(request):
    navBar = navBarFunc(True)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('modify')
    
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form, 'navBar': navBar}
        return render(request, 'edit_profile.html', args)


def password(request):
    navBar = navBarFunc(True)

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('modify')
        else:
            return redirect('/modify/password')
    else: 
        form = PasswordChangeForm(user=request.user)
        args = {'form': form, 'navBar': navBar}
        return render(request, 'password.html', args)

def del_user(request):
    # User must be logged in to access modify page
    navBar = navBarFunc(True)
	
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        
        if form.is_valid():
            rem = User.objects.get(username=form.cleaned_data['username'])
            if rem is not None:
                rem.delete()
                return redirect ('index.html')
                                
            else:
                return redirect('del_user.html')
                
    else:
        form = DeleteUserForm()
        context = {'form': form, 'navBar' : navBar}
        return render(request, 'del_user.html', context)
    
    
def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['sendto_email'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('email')
    return render(request, "email.html", {'form': form})

def thanks(request):
    return HttpResponse('Thank you for your message.')
