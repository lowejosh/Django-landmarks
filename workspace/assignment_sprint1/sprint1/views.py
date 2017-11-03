from django.contrib.auth import login, authenticate, update_session_auth_hash
from sprint1.forms import SignUpForm, EditProfileForm, EmailForm, DeleteUserForm, ContactForm, ReviewForm, PostImage, SuggestLocationForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignUpForm, EditProfileForm, DeleteUserForm, EmailForm, BugForm, ContactForm, ReviewForm
from .models import Location, Profile, Review, Bug, Subscription

# Navbar function that returns the proper list
def navBarFunc(request):
    if (request.user.is_authenticated()):
        toolbar = '<ul><li><a href="/">Home</a></li><li><a href="/suggestLocation/">Suggest Location</a></li><li class="right"><a href="/logout/">Log out</a></li><li><a href="/location/">Locations</a></li><li class="right"><a href="/modify/">Modify Account</a></li><li class="right"><a href="/email/">Referral</a></li><li class="right"><a href="/bugs/">Bug Report</a></li></ul>'

        if (request.session.get('admin', None) == True):
            return '<button onclick="location.href=\'http://127.0.0.1:8000/admin/login/?next=/admin/\'" style="position:absolute; top: 10px; right: 10px;" class="button">Admin</button>' + toolbar
        else :
            return toolbar
    else:
        return '<ul><li><a href="/">Home</a></li><li class="right"><a href="/login/">Log in</a></li><li class="right"><a href="/signup/">Register</a></li><li class="right"><a href="/bugs/">Bug Report</a></li></ul>'


# Review HTML output function
def ReviewOutput(location):

    # Try to find a review for the location input
    try:
        r = Review.objects.filter(location=Location.objects.get(id=location))
    # If no review
    except:
        return ""

    # Defaults
    ReviewList = []
    starRating = []
    

    # For every review - append the star checkbox HTML output into a list
    for i in range(0, r.count()):
        if r[i].rating == 1:
            print(r[i].user.id)
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

    # For every review - append the full HTML output into the review list
    for i in range(0, r.count()):
        ReviewList.append("""<table class="info" width="80%" align="center">
            <tr>
                <td>
                    <span class="review-name"><a href='/profile/""" + str(r[i].user.id) + """'>""" + str(r[i].user) + """</a> said:</span>
                    <div class="rate">
                    """ + starRating[i] + """
                    </div><br />
                    <div class="rating-text">
                    """ + str(r[i].reviewText) + """
                    </div>
                </td>
            </tr>
        </table><br />""")

    # Return a list of the HTML output
    return ReviewList



# Function that returns the html output of a location
def locationOutput(locationId, search_query, checkedOptions):
    # Try to see if a location matches the search query
    try:
        l = Location.objects.get(id=locationId, locationName__contains=search_query)
    # If no results
    except:
        return ""

    # For every checked option filter
    for i in checkedOptions:

        # If the location type matches the filter
        if l.locationType == i:
            locationName = l.locationName
            locationBio = l.locationBio
            locationSt = l.locationAddress
            locationType = locationTypeOutput(l.locationType)
            linkId = str(locationId)

            # Return the HTML output
            return """
                <div class='location-wrap'>
                    <a class="location-name" href="/location/individual/""" + linkId + """">""" + locationName + """<span style="float: right; color: #FCFCFC; margin-right: 6px;">""" + locationType + """</span></a>
                    <span class='location-bio'>""" + locationSt + """</span>
                </div>
            """

    # If there are no results at all
    return ""


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

# Simple map location object grabber
def mapOutput(locationId, search_query, checkedOptions):
    # Try to search locations matching search query
    try:
        l = Location.objects.get(id=locationId, locationName__contains=search_query)
    except:
        return None

    # Filter by checked options
    for i in checkedOptions:

        # If its a match
        if l.locationType == i:

            # Return location
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

# Suggest location view
def suggestLocation(request):

    # Define the navbar
    if (request.user.is_authenticated()):
        navBar = navBarFunc(request)
        # Retrieve information if a review has been submitted
        if request.method == 'POST':
            form = SuggestLocationForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                notification = "Your location suggestion has been submitted"
                context_dict = {'navBar' : navBar, 'notification' : notification,}
                # Return a notification if the form succeeds
                return render(request, 'notification.html', context=context_dict)
        else:
            # Render the form if the method isnt POST (form not submitted)
            form = SuggestLocationForm()
        # in any case render the page
        return render(request, 'suggestLocation.html', {'form': form, 'navBar' : navBar,})
    else:
        navBar = navBarFunc(request)
        notification = 'You need to be logged in to view this page. Log in <a href="/login/">here</a>.'
        context_dict = {'navBar' : navBar, 'notification' : notification}
        return render(request, 'notification.html', context=context_dict)
    

# Profile view
def profile(request, user_id): 
    
    # Show the correct navBar
    if (request.user.is_authenticated()):
        navBar = navBarFunc(request)
    else:
        navBar = navBarFunc(request)

    try:
        # Retrieve data from database
        l = Profile.objects.get(id=int(user_id))
        username = l.user
        firstName = l.firstName
        gender = l.gender
        accountType = l.accountType
        dateofbirth = l.dateOfBirth
        context_dict = {'navBar' : navBar, 'username' : username, 'firstName': firstName, 'gender': gender, 'accountType': accountType, 'dateofbirth': dateofbirth}
        return render(request, 'profile.html', context=context_dict)
    except:
        # If there is no data
        notification = "This user does not exist"
        context_dict = {'navBar' : navBar, 'notification' : notification,}
        return render(request, 'notification.html', context=context_dict)


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
            notification = 'Your review has been successfully submitted'
            context_dict = {'navBar' : navBar, 'notification' : notification}
            return render(request, 'notification.html', context=context_dict)

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
    accountType = 0
    invisibleStyle = "style='display: none;'"
    locationList = []
    pointsList = []
    checked1 = checked2 = checked3 = checked4 = checked5 = "checked"
    style1 = style2 = style3 = style4 = style5 = ""
    notif = ""


    # If the user is logged in
    if (request.user.is_authenticated()):

        # maybe disable the checkboxes instead and add a little notification
        # 1 - Student (universities, libraries), 2 - Business (hotels, libraries), 3 - Tourist (public places, museums)
        accountType = Profile.objects.get(user=(request.user)).accountType

        navBar = navBarFunc(request)

    else:
        navBar = navBarFunc(request)
        notification = 'You need to be logged in to view this page. Log in <a href="/login/">here</a>.'
        context_dict = {'navBar' : navBar, 'notification' : notification}
        return render(request, 'notification.html', context=context_dict)

    checkedOptions = list(map(int, request.GET.getlist("foo", [])))

    # default checks
    if accountType == "1":
        checked2 = "disabled"
        checked4 = "disabled"
        checked5 = "disabled"
        notif = "<p style='margin-top: 12px'>As a student account, you can only search for libraries and universities, to view others, you need to upgrade to our premium plan</p>"
    elif accountType == "2":
        checked3 = "disabled"
        checked4 = "disabled"
        checked5 = "disabled"
        notif = "<p style='margin-top: 12px'>As a business account, you can only search for libraries and hotels, to view others, you need to upgrade to our premium plan</p>"
    elif accountType == "3":
        checked1 = "disabled"
        checked2 = "disabled"
        checked3 = "disabled"
        notif = "<p style='margin-top: 12px'>As a tourist account, you can only search for museums and public places, to view others, you need to upgrade to our premium plan</p>"


    # If someone searches
    if request.method == 'GET':
        search_query = request.GET.get('search-box', "")
        if request.GET.getlist("foo"):

            # 'nother default if the list exists
            checked1 = checked2 = checked3 = checked4 = checked5 = ""

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

                if accountType == "1":
                    checked2 = "disabled"
                    checked4 = "disabled"
                    checked5 = "disabled"
                    notif = "<p style='margin-top: 12px'>As a student account, you can only search for libraries and universities, to view others, you need to upgrade to our premium plan</p>"
                elif accountType == "2":
                    checked3 = "disabled"
                    checked4 = "disabled"
                    checked5 = "disabled"
                    notif = "<p style='margin-top: 12px'>As a business account, you can only search for libraries and hotels, to view others, you need to upgrade to our premium plan</p>"
                elif accountType == "3":
                    checked1 = "disabled"
                    checked2 = "disabled"
                    checked3 = "disabled"
                    notif = "<p style='margin-top: 12px'>As a tourist account, you can only search for museums and public places, to view others, you need to upgrade to our premium plan</p>"




    locationMax = 50;
    # For every location
    for i in range(1, Location.objects.count() + 1):
        # If the max amount hasnt been reached
        if i <= locationMax:
            # Add the location to the location list
            locationList.append(locationOutput(i, search_query, checkedOptions))
            if mapOutput(i, search_query, checkedOptions) != None:
                # Add the location object to the points list
                pointsList.append(mapOutput(i, search_query, checkedOptions))

    coordinateList = []
    # For every location in the points list, retrieve the lat and lon and append it into a multi-dimensional list
    for i in pointsList:
        coordinateList.append([i.latitude, i.longitude])

    # Show error if there are no results
    errorMessageCount = 0
    for i in range(1, Location.objects.count() + 1):
        if (locationOutput(i, search_query, checkedOptions) != ""):
            errorMessageCount+=1

    if errorMessageCount == 0:
        errorMessage = "<span class='no-location-error'>Press Search to view available locations</span>"
    else:
        errorMessage = ""


    # Define the context of the python vars
    context_dict = {'notif': notif, 'points': pointsList, 'checked1': checked1, 'checked2': checked2, 'checked3': checked3, 'checked4': checked4, 'checked5': checked5, 'navBar' : navBar, 'errorMessage': errorMessage, 'locationList': locationList,}

    # Return the template
    return render(request, 'locationfeed.html', context=context_dict)


# Modify view which has a nav bar and fail safe user logged in function
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


# Edit Profile function which updates database with the user details entered by the user
def edit_profile(request):
    navBar = navBarFunc(request)

    if (request.user.is_authenticated()):
        # If send button pressed, send the forms inputs to the database and update
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                return redirect('modify')
        # If send button not pressed, continue to display a input edit form and nav bar
        else:
            form = EditProfileForm(instance=request.user)
            args = {'form': form, 'navBar': navBar}
            return render(request, 'edit_profile.html', args)
    else:
        navBar = navBarFunc(request)
        notification = 'You need to be logged in to view this page. Log in <a href="/login/">here</a>.'
        context_dict = {'navBar' : navBar, 'notification' : notification}
        return render(request, 'notification.html', context=context_dict)

# Password function which updates the password for that user if they opt to change it
def password(request):
    navBar = navBarFunc(request)
    if (request.user.is_authenticated()):
        # If send button pressed, send the forms inputs to the database and update
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('modify')
            else:
                return redirect('/modify/password')
        # If send button not pressed, continue to display a input password form and nav bar
        else:
            form = PasswordChangeForm(user=request.user)
            args = {'form': form, 'navBar': navBar}
            return render(request, 'password.html', args)
    else:
        navBar = navBarFunc(request)
        notification = 'You need to be logged in to view this page. Log in <a href="/login/">here</a>.'
        context_dict = {'navBar' : navBar, 'notification' : notification}

# Delete User function which deletes the user account from the system
def del_user(request):

    navBar = navBarFunc(request)
    # If send button pressed, send the forms inputs to the database and update
    if (request.user.is_authenticated()):
        if request.method == 'POST':
            form = DeleteUserForm(request.POST)

            if form.is_valid():
                rem = User.objects.get(username=form.cleaned_data['username'])
                if rem is not None:
                    rem.delete()
                    return redirect ('../../login')
                else:
                    return redirect('del_user.html')
        # If send button not pressed, continue to display a input delete form and nav bar
        else:
            form = DeleteUserForm()
            context = {'form': form, 'navBar' : navBar}
            return render(request, 'del_user.html', context)
    else:
        navBar = navBarFunc(request)
        notification = 'You need to be logged in to view this page. Log in <a href="/login/">here</a>.'
        context_dict = {'navBar' : navBar, 'notification' : notification}
        return render(request, 'notification.html', context=context_dict)

# Email function which sends a generated email message to the specified email that the user input
def email(request):
    navBar = navBarFunc(request)
    if (request.user.is_authenticated()):
        form = EmailForm(request.POST)
        # If send button pressed, send the forms inputs to the database and also a email to the recipient
        if form.is_valid():
            sendEmail([form.cleaned_data['email']])
            return redirect('email')
        context = {'form': form, 'navBar': navBar}
        return render(request, "email.html", context)
    else:
        navBar = navBarFunc(request)
        notification = 'You need to be logged in to view this page. Log in <a href="/login/">here</a>.'
        context_dict = {'navBar' : navBar, 'notification' : notification}
        return render(request, 'notification.html', context=context_dict)


def sendEmail(to_email):
    subject = "Your friend is asking you to join 'The Good Guys'"
    message = "Hello, your friend is asking you to join us. Please sign up following this link - http://127.0.0.1:8000/signup/"
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, to_email, fail_silently=False)

# Imageform function which saves images to the database that the users upload
def imageform(request):
    navBar = navBarFunc(request)
    if (request.user.is_authenticated()):
        form = PostImage(request.POST, request.FILES or None)
        # If send button pressed, send the forms inputs to the database and update
        if form.is_valid():
            form.save()
            return redirect('imageform')
        # If send button not pressed, continue to display a input image form and nav bar
        else:
            context = {'form': form, 'navBar': navBar}
            return render(request, 'imageform.html', context)
    else:
        navBar = navBarFunc(request)
        notification = 'You need to be logged in to view this page. Log in <a href="/login/">here</a>.'
        context_dict = {'navBar' : navBar, 'notification' : notification}
        return render(request, 'notification.html', context=context_dict)

def bugs(request):
    navBar = navBarFunc(request)
    form = BugForm(request.POST)
    if form.is_valid():
        formSubject = form.cleaned_data['subject']
        formDescription = form.cleaned_data['description']
        bugReport = Bug.objects.create(subject = formSubject, description = formDescription)
        #return redirect('bugs')
        notification = 'Your bug has been successfully submitted'
        context_dict = {'navBar' : navBar, 'notification' : notification}
        return render(request, 'notification.html', context=context_dict)
    context = {'form': form, 'navBar': navBar}
    return render(request, "bugs.html", context)


def subscription(request):
    navBar = navBarFunc(request)
    context = {'navBar': navBar}
    return render(request, "subscription.html", context)

def subscribe(request):
    #Retrive Email Address of User
    username = request.user
    userQuery = Profile.objects.get(user = username)

    #Determine if already subscribed
    if Subscription.objects.filter(firstName = userQuery.firstName, email = userQuery.email, accountType = userQuery.accountType).exists() == False:
        #Subscribe
        subscriptionReport = Subscription.objects.create(firstName = userQuery.firstName, email = userQuery.email, accountType = userQuery.accountType)
    return redirect('modify')

def unsubscribe(request):
    #Retrive Email Address of User
    username = request.user
    userQuery = Profile.objects.get(user = username)

    #Determine if already subscribed
    if Subscription.objects.filter(firstName = userQuery.firstName, email = userQuery.email, accountType = userQuery.accountType).exists() == True:
        #Subscribe
        subscriptionReport = Subscription.objects.filter(firstName = userQuery.firstName, email = userQuery.email, accountType = userQuery.accountType).delete()
    return redirect('modify')

def changelog(request):
    navBar = navBarFunc(request)
    context = {'navBar': navBar}
    return render(request, 'ChangeLOG.html', context)

def TOS(request):
    navBar = navBarFunc(request)
    context = {'navBar': navBar}
    return render(request, 'ToS.html', context)
