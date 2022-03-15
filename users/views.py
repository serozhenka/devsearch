from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Message
from .forms import UserRegisterForm, ProfileForm, SkillForm, MessageForm
from . import utils

def profilesPage(request):
    profiles = utils.searchProfiles(request)
    profiles, paginator, custom_range = utils.paginateProfiles(request, profiles, results=3)

    return render(request, 'users/profiles.html', context={
        'profiles': profiles,
        'paginator': paginator,
        'custom_range': custom_range,
    })

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
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'This username does not exists')
            return render(request, 'users/login_register.html', context={'pageName': 'login'})

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(request.GET.get('next') if 'next' in request.GET else 'profiles')
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

@login_required(login_url='login')
def inbox(request):
    message_objects = request.user.profile.messages.all()
    unread_count = message_objects.filter(is_read=False).count()
    return render(request, 'users/inbox.html', context={
        'message_objects': message_objects,
        'unread_count': unread_count,
    })

@login_required(login_url='login')
def messagePage(request, pk):
    try:
        message_object = request.user.profile.messages.all().get(id=pk)
    except:
        return HttpResponse('<h1>You are not allowed to read someone\'s messages</h1>')

    if not message_object.is_read:
        message_object.is_read = True
        message_object.save()

    return render(request, 'users/message.html', context={'message': message_object})

def send_message(request, pk):
    recipient = Profile.objects.get(id=pk)

    if request.method == "GET":
        form = MessageForm()
    elif request.method == "POST":
        sender = request.user.profile if request.user.is_authenticated else None

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.recipient = recipient
            message.sender = sender

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            return redirect('user-profile', pk)

    return render(request, 'users/message_form.html', context={'recipient': recipient, 'form': form})

