from django.contrib import admin
from .models import Profile, Location, Review, Tag, LocationSuggestion, PostImage

from django.contrib import admin, messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Profile, Location, Review, User, Tag, LocationSuggestion, AdminViewer, EmailForm, Bug

# Function to allow admins to solve bugs
def AcceptBug(modeladmin, request, queryset):
    modeladmin.message_user(request, "You have accepted " + str(queryset.count()) + " bugs as being solved.")
    for entry in queryset:
        Bug.objects.filter(id=entry.id).delete();
AcceptBug.short_description = "Accept Bugs as Solved"

# Function to allow admins to remove bugs
def RemoveBug(modeladmin, request, queryset):
    modeladmin.message_user(request, "You have removed " + str(queryset.count()) + " bugs.")
    for entry in queryset:
        Bug.objects.filter(id=entry.id).delete();
RemoveBug.short_description = "Remove Invalid Bugs"

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

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'firstName', 'lastName', 'gender', 'accountType', 'dateOfBirth', 'email', 'phoneNumber', 'address']

class ProfileBug(admin.ModelAdmin):
    list_display = ['subject', 'description']
    actions = [AcceptBug, RemoveBug]
    # Remove default delete bugs action
    del actions[0]

class AdminViewerFuntion(admin.ModelAdmin):
    actions = [AutoLogin]
    # Remove default remove user action
    del actions[0]

admin.site.register(EmailForm)
admin.site.register(PostImage)

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(LocationSuggestion)
admin.site.register(Bug, ProfileBug);
admin.site.register(AdminViewer, AdminViewerFuntion)

