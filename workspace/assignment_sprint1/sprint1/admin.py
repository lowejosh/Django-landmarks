from django.contrib import admin
from .models import Profile, Location, Review, Tag, LocationSuggestion, PostImage

from django.contrib import admin, messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.db.models.aggregates import Count
from random import randint
from .views import sendEmail
from .models import Profile, Location, Review, User, Tag, LocationSuggestion, AdminViewer, EmailForm, Bug, Subscription

# Function to allow admins to solve bugs
def AcceptBug(modeladmin, request, queryset):
    modeladmin.message_user(request, "You have accepted " + str(queryset.count()) + " bugs as being solved.")
    for entry in queryset:
        Bug.objects.filter(id=entry.id).delete()
AcceptBug.short_description = "Accept Bugs as Solved"

# Function to allow admins to remove bugs
def RemoveBug(modeladmin, request, queryset):
    modeladmin.message_user(request, "You have removed " + str(queryset.count()) + " bugs.")
    for entry in queryset:
        Bug.objects.filter(id=entry.id).delete()
RemoveBug.short_description = "Remove Invalid Bugs"

# Function to allow admins to remove location suggestions
def RemoveLocationSuggestion(modeladmin, request, queryset):
    modeladmin.message_user(request, "You have removed " + str(queryset.count()) + " location suggestions.")
    for entry in queryset:
        LocationSuggestion.objects.filter(id=entry.id).delete()
RemoveLocationSuggestion.short_description = "Removes suggested location"

# Function to allow admins to accept location suggestions
def AcceptLocationSuggestion(modeladmin, request, queryset):
    modeladmin.message_user(request, "You have added " + str(queryset.count()) + " location suggestions to the primary database")
    for entry in queryset:
        sl = LocationSuggestion.objects.filter(id=entry.id)
        l = Location(locationName = sl.locationName, latitude = sl.latitude, longitude = sl.longitude, locationBio = sl.locationBio, locationAddress = sl.locationAddress, locationType = sl.locationType, locationImagePath = "/")
        l.save()
        sl.delete()
        
RemoveLocationSuggestion.short_description = "Moves suggested location into the primary location database"

# Function to allow admins to login as the selected user
def AutoLogin(modeladmin, request, queryset):
    if queryset.count() != 1:
        modeladmin.message_user(request, "Cannot login into more than one account", level=messages.ERROR)
        return

    user = queryset[0].user
    login(request, user)
    request.session['admin'] = True
    return redirect('index')
AutoLogin.short_description = "Login as User"

def SendNewsletter(modeladmin, request, queryset):
    #Retrieve Random List of Locations
    touristSelection = Location.objects.filter(locationType = 4)
    touristCount = randint(0, touristSelection.aggregate(count=Count('locationName'))['count'] - 1)
    studentSelection = Location.objects.filter(locationType = 1)
    studentCount = randint(0, studentSelection.aggregate(count=Count('locationName'))['count'] - 1)
    businessmanSelection = Location.objects.filter(locationType = 2)
    businessmanCount = randint(0, businessmanSelection.aggregate(count=Count('locationName'))['count'] - 1)
    premiumCount = randint(0, Location.objects.aggregate(count=Count('locationName'))['count'] - 1)

    #Add all people to email list
    for entry in queryset:
        print(entry.accountType)
        #Student
        if entry.accountType == '1':
            location = studentSelection[studentCount].locationName
        #Business
        if entry.accountType == '2':
            location = businessmanSelection[studentCount].locationName
        #Tourist
        if entry.accountType == '3':
            location = touristSelection[studentCount].locationName

        #Send Email
        subject = "Newsletter"
        message = "Hello, we have chosen a location that may be interesting to you. " + location + " is an amazing place to visit!"
        to_email = [entry.email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, to_email, fail_silently=False)

    #Show Email has been sent
    modeladmin.message_user(request, "Newsletter has been sent to all selected users")

SendNewsletter.short_description = "Send Newsletter"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'firstName', 'lastName', 'gender', 'accountType', 'dateOfBirth', 'email', 'phoneNumber', 'address']

class ProfileBug(admin.ModelAdmin):
    list_display = ['subject', 'description']
    actions = [AcceptBug, RemoveBug]

class LocationAcceptDeny(admin.ModelAdmin):
    actions = [RemoveLocationSuggestion, AcceptLocationSuggestion]

class AdminViewerFuntion(admin.ModelAdmin):
    actions = [AutoLogin]

class LocationSuggestionFunction(admin.ModelAdmin):
    list_display = ['firstName', 'accountType', 'email']
    actions = [SendNewsletter]

admin.site.register(EmailForm)
admin.site.register(PostImage)

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(LocationSuggestion, LocationAcceptDeny)
admin.site.register(Bug, ProfileBug)
admin.site.register(AdminViewer, AdminViewerFuntion)
admin.site.register(Subscription, LocationSuggestionFunction)
