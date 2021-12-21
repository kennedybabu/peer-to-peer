from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.fields import DateTimeField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='posts/', null=True)

    def save_profile(self):
        '''
        save profile
        '''
        self.save()

    def delete_profile(self):
        '''
        delete profile
        '''
        self.delete()

    def update_profile(self, new):
        '''
        method that will update the profile
        '''
        self.username = new.username
        self.bio = new.bio
        self.profile_photo = new.profile_photo
        self.save()  


    @receiver(post_save,sender=User)
    def create_user_profile(sender,instance,created, **kwargs):
        if created:
            Profile.objects.create(user_id=instance)

    @receiver(post_save,sender=User)
    def save_profile(sender,instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.username 


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250)
    repo_link = models.CharField(max_length=500)
    live_link = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='posts', null=True)

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



