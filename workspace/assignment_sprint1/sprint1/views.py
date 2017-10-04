from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from sprint1.models import Location
# Signup imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from sprint1.forms import SignUpForm, EditProfileForm, EmailForm, DeleteUserForm, ContactForm

from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

# Navbar function that returns the proper list 
def navBarFunc(request, isLogged): 
    if (isLogged):
        if (request.session.get('admin', None) == True):
            return '<button onclick="location.href=\'http://127.0.0.1:8000/admin/login/?next=/admin/\'" style="position:absolute; top: 10px; right: 10px;" class="button">Admin</button><ul><li><a href="/">Home</a></li><li class="right"><a href="/logout/">Log out</a></li><li><a href="/location/page-1">Locations</a></li><li class="right"><a href="/modify/">Modify Account</a></li></ul>'
        else :
            return '<ul><li><a href="/">Home</a></li><li class="right"><a href="/logout/">Log out</a></li><li><a href="/location/page-1">Locations</a></li><li class="right"><a href="/modify/">Modify Account</a></li></ul>'
    else:
        return '<ul><li><a href="/">Home</a></li><li class="right"><a href="/login/">Log in</a></li><li class="right"><a href="/signup/">Register</a></li><li><a href="/location/page-1">Locations</a></li></ul>'

# Function that returns the html output of a location
#TODO
def locationOutput(locationId, search_query):
    try:
        l = Location.objects.get(id=locationId, locationName__contains=search_query)
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

def returnSearch(search_query):
    return Location.objects.filter(locationName__contains=search_query).values_list('id', flat=True)
    


# Index page view
def index(request):
    # If the user is logged in
    if (request.user.is_authenticated()):
        # Define the navbar to only show logout button
        navBar = navBarFunc(request, True)   
        # Define the context of the python vars
        context_dict = {'navBar' : navBar,}
        # Return the template
        return render(request, 'privateMain.html', context=context_dict)
        # If the user isn't logged in
    else:
        # Define the navbar to show login button
        navBar = navBarFunc(request, False) 
        # Define the context of the python vars
        context_dict = {'navBar' : navBar,}
        # Return the template
        return render(request, 'publicMain.html', context=context_dict)
        

# Signup page view
def signup(request):

    # Define the navbar
    navBar = navBarFunc(request, False)

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
        navBar = navBarFunc(request, True)
    else:
        navBar = navBarFunc(request, False)

    # Define the context of the python vars
    context_dict = {'navBar' : navBar, 'location_id' : location_id,}

    # Return the template
    return render(request, 'viewLocation.html', context=context_dict)

    
# Location Feed
def locationfeed(request, page):
    
    # Default Search Query
    search_query = ""

    # To normalize it (yeah i know)
    page = int(page) - 1

    # Defaults
    location1 = locationOutput(1, search_query)
    location2 = ""
    location3 = ""
    location4 = ""
    location5 = ""
    location6 = ""
    location7 = ""
    location8 = ""


    #TODO
    # If someone searches
    if request.method == 'GET':
        search_query = request.GET.get('search-box', "")
        resultIds = returnSearch(search_query)
#        d={}

        testingBox = resultIds
        
        location1 = locationOutput(1, search_query)
        location2 = locationOutput(2, search_query)
        location3 = locationOutput(3, search_query)
        location4 = locationOutput(4, search_query)
        location5 = locationOutput(5, search_query)
        location6 = locationOutput(6, search_query)
        location7 = locationOutput(7, search_query)
        location8 = locationOutput(8, search_query)


#        count = 0
#        if resultIds.count() > 0:
#            for i in resultIds:
#                if count < 8:
#                    d["location{0}".format(count + 1)] = locationOutput(resultIds[count])
#                    count+=1
#
    else:
        testingBox = ""


    # Display the new results



    # Show error if there are no results
    if (locationOutput(page * 8 + 1, search_query) == ""):
        errorMessage = "<span class='no-location-error'>Sorry, there are no locations matching your search</span>"
    else:
        errorMessage = ""
        
    # Show next page button if there exists a location on the next page
    # TODO THIS WILL BREAK
    if (locationOutput((page + 1) * 8 + 1, search_query) != ""):
        nextPage = '<span class="next-page"><a class="pretty-button" href="/location/page-' + str(page + 2) + '">Next page?</a></button></span>'
    else:
        nextPage = ""

    # Show the correct navBar
    if (request.user.is_authenticated()):
        navBar = navBarFunc(request, True)
    else:
        navBar = navBarFunc(request, False)

    
    # TEMPORARY
#   location1 = locationOutput(page * 8 + 1)
#    location2 = locationOutput(page * 8 + 2)
#    location3 = locationOutput(page * 8 + 3)
#    location4 = locationOutput(page * 8 + 4)
#    location5 = locationOutput(page * 8 + 5)
#    location6 = locationOutput(page * 8 + 6)
#    location7 = locationOutput(page * 8 + 7)
#    location8 = locationOutput(page * 8 + 8)

    # Define the context of the python vars
    context_dict = {'testingBox': testingBox, 'navBar' : navBar, 'errorMessage': errorMessage, 'page': page + 1, 'nextPage': nextPage, 'location1': location1, 'location2': location2, 'location3': location3,'location4': location4,'location5': location5,'location6': location6,'location7': location7,'location8': location8,}

    # Return the template
    return render(request, 'locationfeed.html', context=context_dict)

def modify(request):
    # User must be logged in to access modify page
    navBar = navBarFunc(request, True)
	
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'navBar' : navBar}
	
    return render(request, 'modify.html', context=context_dict)


def edit_profile(request):
    navBar = navBarFunc(request, True)

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
    navBar = navBarFunc(request, True)

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
    navBar = navBarFunc(request, True)
	
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
    navBar = navBarFunc(request, True)
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
    context = {'form': form, 'navBar': navBar}
    return render(request, "email.html", context)

def thanks(request):
    return HttpResponse('Thank you for your message.')
