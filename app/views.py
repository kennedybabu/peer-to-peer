# from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from .models import  Project, Rate, User
# from django.contrib.auth.forms import UserCreationForm
from .forms import NewProjectForm, RateProjectForm, MyUserCreationForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib  import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



# Create your views here.

def logoutUser(request):
    logout(request)
    return redirect('login')        


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


def register_user(request):
    form = MyUserCreationForm()
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'an error occurred during registration')

    context = {
        'form':form
    }
    return render(request, 'registration/register_user.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render('home')
        else:
            messages.error(request, 'username or password does not exist')


    context = {

    }
    return render(request, 'registration/login.html', context)


@login_required(login_url='login')
def view_profile(request , pk):
    user = User.objects.get(id=pk)
    posts = Project.objects.all()
    projects = user.project_set.all()
    context = {
        'projetcs':projects,
        'posts':posts,
        'user':user
    }   
    return render(request, 'profile.html', context)


def update_profile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_profile', pk=user.id)
    context = {
        'form':form
    }
    return render(request, 'update_profile.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects':projects})


@login_required(login_url='login')
def rate_project(request, id):
    current_user = request.user
    try:
        project = Project.objects.get(id = id)
    except ObjectDoesNotExist:
        raise Http404()
    ratings = project.rate_set.all()

    if request.method == 'POST':
        form = RateProjectForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.owner = current_user
            rating.project = project
            rating.save()
            return redirect('home')
    else:
        form = RateProjectForm()   
    
    return render(request, 'rate_project.html', {'project':project, 'form':form , 'ratings':ratings})