# from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .forms import NewProjectForm
from django.contrib.auth import authenticate, login, logout
from django.contrib  import messages


# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, 'request successful')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register_user.html', {'form':form})

    
def login_user(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(request, username = username, password  = password) 

       if user is not None:
           login(request, user)
           return redirect('home')
       else:
           messages.success(request, 'There was a error in the request. Try again')
           return redirect('login')

    else:
        return render(request, 'registration/register_user.html')


def logoutUser(request):
    logout(request)
    return redirect('login')        


def home(request):
    return render(request, 'home.html')


def view_profile(request, id):
    try:
        profile = Profile.objects.get(id = id)
        context = {
            'profile': profile,                       
        }
        return render(request, 'profile.html', context)
    except:
        messages.warning(request, 'Sorry, but it seems the profile is not set up')
        return redirect('home')


# def profile(request):
#     profiles = Profile.objects.all()
#     return render(request, 'profile.html', {'profiles': profiles})


def new_project(request):
    current_user = request.user
    if request.method == "POST":
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = current_user
            project.save()
        return redirect('home')
    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {'form':form})