from django.db import models
# models.py
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    email = models.CharField(max_length=200, null=True)
    zipCode = models.IntegerField()
    mobile = models.CharField(max_length=120, unique=True)
    walking = models.CharField(max_length=200)
    running = models.CharField(max_length=200)
    gardening = models.CharField(max_length=200, null=True)
    swimming = models.CharField(max_length=200)
    coffeeTea = models.CharField(max_length=200, null=True)
    foodGathering = models.CharField(max_length=200, null=True)
    televisionSports = models.CharField(max_length=200, null=True)
    movies = models.CharField(max_length=200, null=True)
    shopping = models.CharField(max_length=200, null=True)
    happyHours = models.CharField(max_length=200, null=True)
    errands = models.CharField(max_length=200, null=True)
    rides = models.CharField(max_length=200, null=True)
    childcare = models.CharField(max_length=200, null=True)
    eldercare = models.CharField(max_length=200, null=True)
    petcare = models.CharField(max_length=200, null=True)
    tutoring = models.CharField(max_length=200, null=True)
    repairAdvice = models.CharField(max_length=200, null=True)
    otherAdvice = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    sharePreference = models.CharField(max_length=200, null=True)

def __str__(self):
        return self.user.username

# Create your models here.
