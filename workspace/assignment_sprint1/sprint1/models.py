# Imports
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm

# Profile Model
class Profile(models.Model):
    # Model the table fields
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=63, null=True)
    lastName = models.CharField(max_length=63, null=True)
    gender = models.CharField(max_length=31, null=True)
    accountType = models.CharField(max_length=31, null=True)
    dateOfBirth = models.DateField(null=True)
    email = models.EmailField(max_length=254, null=True)
    phoneNumber = models.CharField(max_length=31, null=True, blank=True)
    address = models.CharField(max_length=254, null=True)

    # Define string representation
    def __str__(self):
        return self.user.username

class Location(models.Model):
    # The primary key is automatically created if not specified (id)
    locationName = models.CharField(max_length=254, null=True)
    latitude = models.IntegerField(null=True)
    longtiude = models.IntegerField(null=True)
    locationAddress = models.CharField(max_length=254, null=True)
    locationBio = models.TextField(max_length=511, null=True)
    locationType = models.IntegerField(null=True)
    locationImagePath = models.CharField(max_length=127, null=True) 

class Review(models.Model):
    user = models.ForeignKey(Profile)
    location = models.ForeignKey(Location)
    reviewText = models.TextField(max_length=1023)
    rating = models.IntegerField(null=True)

class Image(models.Model):
    location = models.ForeignKey(Location)
    imagePath = models.CharField(max_length=127)

class Tag(models.Model):
    location = models.ForeignKey(Location)
    tagText = models.CharField(max_length=254)

# Create and update user from signal
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



