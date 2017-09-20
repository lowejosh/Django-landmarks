from django.contrib import admin
from .models import Profile, Location, Review, Tag

# Register your models here.
admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(Tag)

