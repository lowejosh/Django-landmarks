from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignUpForm, EditProfileForm, DeleteUserForm, EmailForm, BugForm, ContactForm, ReviewForm
from .models import Location, Profile, Review, Bug

# Navbar function that returns the proper list
def navBarFunc(request):
    if (request.user.is_authenticated()):
        toolbar = '<ul><li><a href="/">Home</a></li><li class="right"><a href="/logout/">Log out</a></li><li><a href="/location/">Locations</a></li><li class="right"><a href="/modify/">Modify Account</a></li><li class="right"><a href="/email/">Referral</a></li><li class="right"><a href="/bugs/">Bug Report</a></li></ul>'

        if (request.session.get('admin', None) == True):
            return '<button onclick="location.href=\'http://127.0.0.1:8000/admin/login/?next=/admin/\'" style="position:absolute; top: 10px; right: 10px;" class="button">Admin</button>' + toolbar
        else :
            return toolbar
    else:
        return '<ul><li><a href="/">Home</a></li><li class="right"><a href="/login/">Log in</a></li><li class="right"><a href="/signup/">Register</a></li><li class="right"><a href="/bugs/">Bug Report</a></li></ul>'


# Review output function
def ReviewOutput(location):

    try:
        r = Review.objects.filter(location=Location.objects.get(id=location))
    except:
        return ""

    ReviewList = []

    starRating = []

    for i in range(0, r.count()):
        if r[i].rating == 1:
            starRating.append("""
                            <input type="checkbox" id="st1" value="1" /> <!-- 5 Star if checked="checked" -->
                            <label for="st1"></label>
                            <input type="checkbox" id="st2" value="2" />
                            <label for="st2"></label>
                            <input type="checkbox" id="st3" value="3" />
                            <label for="st3"></label>
                            <input type="checkbox" id="st4" value="4" />
                            <label for="st4"></label>
                            <input type="checkbox" id="st5" value="5" checked/>
                            <label for="st5"></label>
                        """)
        elif r[i].rating == 2:
            starRating.append("""
                            <input type="checkbox" id="st1" value="1" /> <!-- 5 Star if checked="checked" -->
                            <label for="st1"></label>
                            <input type="checkbox" id="st2" value="2" />
                            <label for="st2"></label>
                            <input type="checkbox" id="st3" value="3" />
                            <label for="st3"></label>
                            <input type="checkbox" id="st4" value="4" checked/>
                            <label for="st4"></label>
                            <input type="checkbox" id="st5" value="5" />
                            <label for="st5"></label>
                        """)
        elif r[i].rating == 3:
            starRating.append("""
                            <input type="checkbox" id="st1" value="1" /> <!-- 5 Star if checked="checked" -->
                            <label for="st1"></label>
                            <input type="checkbox" id="st2" value="2" />
                            <label for="st2"></label>
                            <input type="checkbox" id="st3" value="3" checked/>
                            <label for="st3"></label>
                            <input type="checkbox" id="st4" value="4" />
                            <label for="st4"></label>
                            <input type="checkbox" id="st5" value="5" />
                            <label for="st5"></label>
                        """)
        elif r[i].rating == 4:
            starRating.append("""
                            <input type="checkbox" id="st1" value="1" /> <!-- 5 Star if checked="checked" -->
                            <label for="st1"></label>
                            <input type="checkbox" id="st2" value="2" checked/>
                            <label for="st2"></label>
                            <input type="checkbox" id="st3" value="3" />
                            <label for="st3"></label>
                            <input type="checkbox" id="st4" value="4" />
                            <label for="st4"></label>
                            <input type="checkbox" id="st5" value="5" />
                            <label for="st5"></label>
                        """)
        elif r[i].rating == 5:
            starRating.append("""
                            <input type="checkbox" id="st1" value="1" checked/> <!-- 5 Star if checked="checked" -->
                            <label for="st1"></label>
                            <input type="checkbox" id="st2" value="2" />
                            <label for="st2"></label>
                            <input type="checkbox" id="st3" value="3" />
                            <label for="st3"></label>
                            <input type="checkbox" id="st4" value="4" />
                            <label for="st4"></label>
                            <input type="checkbox" id="st5" value="5" />
                            <label for="st5"></label>
                        """)

    for i in range(0, r.count()):
        ReviewList.append("""<table class="info" width="80%" align="center">
            <tr>
                <td>
                    <span class="review-name">""" + str(r[i].user) + """ said:</span>
                    <div class="rate">
                    """ + starRating[i] + """
                    </div><br />
                    <div class="rating-text">
                    """ + str(r[i].reviewText) + """
                    </div>
                </td>
            </tr>
        </table><br />""")

    return ReviewList



# Function that returns the html output of a location
def locationOutput(locationId, search_query, checkedOptions):
    try:
        l = Location.objects.get(id=locationId, locationName__contains=search_query)
    except:
        return ""

    for i in checkedOptions:

        if l.locationType == i:
            locationName = l.locationName
            locationBio = l.locationBio
            locationSt = l.locationAddress
            locationType = locationTypeOutput(l.locationType)
            linkId = str(locationId)

            return """
                <div class='location-wrap'>
                    <a class="location-name" href="/location/individual/""" + linkId + """">""" + locationName + """<span style="float: right; color: #FCFCFC; margin-right: 6px;">""" + locationType + """</span></a>
                    <span class='location-bio'>""" + locationSt + """</span>
                </div>
            """

    return ""


# Returns a list of database objects that match the search query
def returnSearch(search_query):
    return Location.objects.filter(locationName__contains=search_query).values_list('id', flat=True)


# Write the location type in plaintext
def locationTypeOutput(locationTypeId):
    # 1 - Library, 2 - Hotel, 3 - University, 4 - Museum, 5 - Public place
    if locationTypeId == 1:
        return "Library"
    elif locationTypeId == 2:
        return "Hotel"
    elif locationTypeId == 3:
        return "University"
    elif locationTypeId == 4:
        return "Museum"
    elif locationTypeId == 5:
        return "Public Space"
    else:
        return ""


# Map Output
def mapOutput(locationId, search_query, checkedOptions):
    try:
        l = Location.objects.get(id=locationId, locationName__contains=search_query)
    except:
        return None

    for i in checkedOptions:

        if l.locationType == i:
            
            return l


# Index page view
def index(request):
    # If the user is logged in
    if (request.user.is_authenticated()):
        # Define the navbar to only show logout button
        navBar = navBarFunc(request)
        # Define the context of the python vars
        context_dict = {'navBar' : navBar,}
        # Return the template
        return render(request, 'publicMain.html', context=context_dict)
        # If the user isn't logged in
    else:
        # Define the navbar to show login button
        navBar = navBarFunc(request)
        # Define the context of the python vars
        context_dict = {'navBar' : navBar,}
        # Return the template
        return render(request, 'publicMain.html', context=context_dict)


# Signup page view
def signup(request):

    # Define the navbar
    navBar = navBarFunc(request)

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

    # Show the correct navBar
    if (request.user.is_authenticated()):
        submitButton = '<button class="pretty-button" type="submit" >Leave Review</button><br />'
        navBar = navBarFunc(request)
    else:
        navBar = navBarFunc(request)
        submitButton = '<button class="pretty-button" type="submit" disabled>Leave Review</button><br /><br /><div class="centered-content">You need to be logged in to submit a review</div>'

    try:
        # Retrieve data from database
        locationId = int(location_id)
        l = Location.objects.get(id=locationId)
        locationName = l.locationName
        locationBio = l.locationBio
        locationAddress = l.locationAddress
        locationTypeId = l.locationType
    except:
        # If there is no data
        notification = "This location does not exist"
        context_dict = {'navBar' : navBar, 'notification' : notification,}
        return render(request, 'notification.html', context=context_dict)

    # DEFAULTS
    tags = ""

    # Render the locationType in plain text
    locationType = locationTypeOutput(locationTypeId)

    # Retrieve information if a review has been submitted
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.location_id = locationId
            instance.user = Profile.objects.get(user=(request.user))
            instance.save()
            return HttpResponseRedirect("")

    else:
        form = ReviewForm()

    ReviewList = ReviewOutput(locationId)



    # Define the context of the python vars
    context_dict = {'submitButton': submitButton, 'form': form, 'ReviewList': ReviewList, 'navBar' : navBar, 'location_id' : location_id, 'locationName': locationName, 'locationBio': locationBio, 'locationAddress': locationAddress, 'locationType': locationType}

    # Return the template
    return render(request, 'viewLocation.html', context=context_dict)


# Location Feed
def locationfeed(request):

    # Default Search Query
    search_query = ""

    # Defaults
    locationList = []
    pointsList = []
    checked1 = "checked"
    checked2 = "checked"
    checked3 = "checked"
    checked4 = "checked"
    checked5 = "checked"

    checkedOptions = list(map(int, request.GET.getlist("foo", [])))

    # If someone searches
    if request.method == 'GET':
        search_query = request.GET.get('search-box', "")
        if request.GET.getlist("foo"):

            # 'nother default if the list exists
            checked1 = ""
            checked2 = ""
            checked3 = ""
            checked4 = ""
            checked5 = ""

            # Save the checked data - because it resets upon submit
            for i in checkedOptions:
                if i == 1:
                    checked1 = "checked"
                elif i == 2:
                    checked2 = "checked"
                elif i == 3:
                    checked3 = "checked"
                elif i == 4:
                    checked4 = "checked"
                elif i == 5:
                    checked5 = "checked"


    locationMax = 50;
    for i in range(1, Location.objects.count() + 1):
        if i <= locationMax:
            locationList.append(locationOutput(i, search_query, checkedOptions))
            if mapOutput(i, search_query, checkedOptions) != None:
                pointsList.append(mapOutput(i, search_query, checkedOptions))

    coordinateList = []
    for i in pointsList:
        coordinateList.append([i.latitude, i.longitude])

    print(coordinateList)

    # Show error if there are no results
    errorMessageCount = 0
    for i in range(1, Location.objects.count() + 1):
        if (locationOutput(i, search_query, checkedOptions) != ""):
            errorMessageCount+=1

    if errorMessageCount == 0:
        errorMessage = "<span class='no-location-error'>Press Search to view available locations</span>"
    else:
        errorMessage = ""

    # Show the correct navBar
    if (request.user.is_authenticated()):
        navBar = navBarFunc(request)
    else:
        navBar = navBarFunc(request)


    # TODO
    # Define the context of the python vars
    context_dict = {'points': pointsList, 'checked1': checked1, 'checked2': checked2, 'checked3': checked3, 'checked4': checked4, 'checked5': checked5, 'navBar' : navBar, 'errorMessage': errorMessage, 'locationList': locationList,}

    # Return the template
    return render(request, 'locationfeed.html', context=context_dict)

def modify(request):
    # User must be logged in to access modify page
    if (request.user.is_authenticated()):
        navBar = navBarFunc(request)
        context_dict = {'navBar' : navBar}
        return render(request, 'modify.html', context=context_dict)
    else:
        navBar = navBarFunc(request)
        notification = 'You need to be logged in to view this page. Log in <a href="/login/">here</a>.'
        context_dict = {'navBar' : navBar, 'notification' : notification}
        return render(request, 'notification.html', context=context_dict)


def edit_profile(request):
    navBar = navBarFunc(request)

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
    navBar = navBarFunc(request)

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
    navBar = navBarFunc(request)

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
    navBar = navBarFunc(request)

    form = EmailForm(request.POST)

    if form.is_valid():
        to_list = [form.cleaned_data['email']]
        subject = "Your friend is asking you to join 'The Good Guys'"
        message = "Hello, your friend is asking you to join us. Please sign up following this link - http://127.0.0.1:8000/signup/"
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        return redirect('email')
    context = {'form': form, 'navBar': navBar}
    return render(request, "email.html", context)

def bugs(request):
    navBar = navBarFunc(request)

    form = BugForm(request.POST)

    if form.is_valid():
        formSubject = form.cleaned_data['subject']
        formDescription = form.cleaned_data['description']
        bugReport = Bug.objects.create(subject = formSubject, description = formDescription)
        return redirect('index')
    context = {'form': form, 'navBar': navBar}
    return render(request, "bugs.html", context)
