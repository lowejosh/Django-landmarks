# Imports
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator

# Bug Model
class Bug(models.Model):
    SUBJECTS = (
        ('A', 'Security'),
        ('B', 'Visual Bug'),
        ('C', 'Feature Not Working'),
        ('D', 'Website Crashing'),
        ('E', 'Other'),
    )
    subject = models.CharField(max_length = 1, choices = SUBJECTS)
    description = models.CharField(max_length = 300)

    # Define string representation
    def __str__(self):
        return self.subject

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
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    locationAddress = models.CharField(max_length=254, null=True)
    locationBio = models.TextField(max_length=511, null=True)
    locationType = models.IntegerField(null=True)
    locationImagePath = models.CharField(max_length=127, null=True)

    # Define string representation
    def __str__(self):
        return self.locationName


ratings = [(1, 1),(2, 2), (3, 3), (4, 4), (5, 5)]

class Review(models.Model):
    user = models.ForeignKey(Profile)
    location = models.ForeignKey(Location)
    reviewText = models.TextField(max_length=1023)
    rating = models.IntegerField(default=1, choices=ratings)

    def __str__(self):
        return "review" + str(self.id)

class Image(models.Model):
    location = models.ForeignKey(Location)
    imagePath = models.CharField(max_length=127)

class Tag(models.Model):
    location = models.ForeignKey(Location)
    tagText = models.CharField(max_length=254)

class LocationSuggestion(models.Model):
    locationName = models.CharField(max_length=254, null=True)
    latitude = models.IntegerField(null=True)
    longitude = models.IntegerField(null=True)
    locationAddress = models.CharField(max_length=254, null=True)
    locationBio = models.TextField(max_length=511, null=True)
    locationType = models.IntegerField(null=True)
    locationImagePath = models.CharField(max_length=127, null=True)

# Create and update user from signal
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class AdminViewer(models.Model):
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

class EmailForm(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
        
 
class PostImage(models.Model):
    title = models.CharField(max_length=120)
    image = models.FileField(null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title
    

