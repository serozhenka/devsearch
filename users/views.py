from django.shortcuts import render
from .models import Profile

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