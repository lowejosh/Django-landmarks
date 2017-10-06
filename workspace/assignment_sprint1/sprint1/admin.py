from django.contrib import admin
from .models import Profile, Location, Review, Tag, Map, LocationSuggestion 
from django.contrib import admin, messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import Profile, Location, Review, Tag, AdminViewer, EmailForm
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from sprint1.models import Location, User
from django.conf import settings

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'firstName', 'lastName', 'gender', 'accountType', 'dateOfBirth', 'email', 'phoneNumber', 'address'] 


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(LocationSuggestion)
admin.site.register(Map)



def autologin(modeladmin, request, queryset):
    if queryset.count() != 1:
        modeladmin.message_user(request, "Cannot login into more than one account", level=messages.ERROR)
        return
            
    user = queryset[0].user
    login(request, user)
    request.session['admin'] = True
    return redirect('index')
        
class AdminViewerFuntion(admin.ModelAdmin):
    actions = [autologin]
    
admin.site.register(AdminViewer, AdminViewerFuntion)

admin.site.register(EmailForm)