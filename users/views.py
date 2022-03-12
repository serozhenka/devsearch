from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegisterForm

def profilesPage(request):
    profiles = Profile.objects.all()
    return render(request, 'users/profiles.html', context={'profiles': profiles, })

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    skills_with_bio = profile.skill_set.exclude(description__exact="")
    skills_without_bio = profile.skill_set.filter(description__exact="")

    return render(request, 'users/user_profile.html', context={
        'profile': profile,
        'skills_with_bio': skills_with_bio,
        'skills_without_bio': skills_without_bio,
    })

def loginPage(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('profiles')

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'This username does not exists')
            return render(request, 'users/login_register.html', context={'pageName': 'login'})

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login_register.html', context={'pageName': 'login'})

def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('profiles')

def registerPage(request):
    if request.method == "GET":
        form = UserRegisterForm()
    elif request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Oops, something went wrong!')

    return render(request, 'users/login_register.html', context={'pageName': 'register', 'form': form})
