from django.shortcuts import render, redirect
from django.http import HttpResponse
# Signup imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from sprint1.forms import SignUpForm, EditProfileForm, EmailForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# Index page view
def index(request):
    # If the user is logged in
    if (request.user.is_authenticated()):
        # Define the navbar to only show logout button
        navBar = '<h5><a href="/logout/">Log out</a><h5><a href="/modify/">Modify Account</a>'
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

def modify(request):
    if (request.user.is_authenticated()):
        # Define the navbar to only show logout button
        navBar = '<h5><a href="/logout/">Log out</a><h5><a href="/modify/">Modify Account</a>'
    # If the user isn't logged in
	
    else:
        # Define the navbar to show login button
        navBar = '<h5><a href="/login/">Log in</a><br /><a href="/signup/">Register</a></h5>'
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'navBar' : navBar}
	
    return render(request, 'modify.html', context=context_dict)


def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		
		if form.is_valid():
			form.save()
			return redirect('modify')
	
	else:
		form = EditProfileForm(instance=request.user)
		args = {'form': form}
		return render(request, 'edit_profile.html', args)


def password(request):
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
		args = {'form': form}
		return render(request, 'password.html', args)

def del_user(request, username):
	try:
		u = User.objects.get(username = username)
		u.delete()
		messages.sucess(request, "The user is deleted")
	except User.DoesNotExist:
		messages.error(request,"User does not exist")
		return render(request, 'index.html')
	return render(request, 'del_user.html')

	
def email(request):	
	if request.method == 'POST':
		form = EmailForm(request.POST)
		
		if form.is_valid():
			save_it = form.save()
			save_it.save()
			subject = 'Come check out the IFB299 Website'
			message = 'Come check out the website: link'
			from_email = settings.EMAIL_HOST_USER
			to_list = ['save_it.email, settings.EMAIL_HOST_USER']
			send_mail(subject, message, from_email, to_list, fail_silently=True)
			return redirect('email')	
	else:
		form = EmailForm()
		args = {'form': form}
		return render(request, 'email.html', args)	
