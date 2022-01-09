from .models import Project, Rate, User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'profile_pic']

        
class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'date_added']


class RateProjectForm(forms.ModelForm):
    class Meta:
        model = Rate
        exclude = ['owner', 'project']