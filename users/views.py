from . import  utils
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserRegisterForm, ProfileForm, SkillForm

def profilesPage(request):
    profiles = utils.searchProfiles(request)

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

@login_required(login_url='login')
def accountPage(request):
    profile = request.user.profile

    return render(request, 'users/account.html', context={
        'profile': profile,
    })

@login_required(login_url='login')
def editAccountPage(request):
    if request.method == "GET":
        form = ProfileForm(instance=request.user.profile)
    elif request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = profile.username.lower()
            profile.save()
            return redirect('account')

    return render(request, 'users/profile_form.html', context={'form': form, })

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
            return redirect('edit-account')
        else:
            messages.error(request, 'Oops, something went wrong!')

    return render(request, 'users/login_register.html', context={'pageName': 'register', 'form': form})

@login_required(login_url='login')
def create_skill(request):
    if request.method == "GET":
        form = SkillForm()
    elif request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            return redirect('account')

    return render(request, 'users/skill_form.html', context={'form': form})


@login_required(login_url='login')
def update_skill(request, pk):
    skillObj = request.user.profile.skill_set.get(id=pk)

    if request.user.profile != skillObj.owner:
        return HttpResponse('<h1>You are not allowed to update someone\'s skill</h1>')

    if request.method == "GET":
        form = SkillForm(instance=skillObj)
    elif request.method == "POST":
        form = SkillForm(request.POST, instance=skillObj)
        if form.is_valid():
            form.save()
            return redirect('account')

    return render(request, 'users/skill_form.html', context={'form': form})

@login_required(login_url='login')
def delete_skill(request, pk):
    skillObj = request.user.profile.skill_set.get(id=pk)

    if request.user.profile != skillObj.owner:
        return HttpResponse('<h1>You are not allowed to delete someone\'s skill</h1>')

    if request.method == "GET":
        return render(request, 'delete_template.html', context={'obj': skillObj})
    elif request.method == "POST":
        skillObj.delete()
        return redirect('account')
