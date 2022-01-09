from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.fields import DateTimeField
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True)
    profile_pic = CloudinaryField('images', null=True, default='user.png')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250)
    repo_link = models.CharField(max_length=500)
    live_link = models.CharField(max_length=500, blank=True)
    image = CloudinaryField('images', null=True)

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()


    def __str__(self):
        return self.name


class Rate(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    design_vote = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    usability_vote = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    content_vote = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)



    def save_rating(self):
        self.save()

    def delete_rating(self):
        self.delete()
        
    def __str__(self):
        return self.owner.username

    @property
    def average_score(self):
        average = (self.design_vote + self.content_vote + self.usability_vote) /3
        return round(average, 1)



