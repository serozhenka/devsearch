from .models import Profile, Skill
from django.db.models import Q

def searchProfiles(request):
    user_query = request.GET.get('user_query') if request.GET.get('user_query') else ''
    profiles = Profile.objects.distinct().filter(
        Q(username__icontains=user_query) |
        Q(name__icontains=user_query) |
        Q(headline__icontains=user_query) |
        Q(location__icontains=user_query) |
        Q(skill__in=Skill.objects.filter(name__icontains=user_query))
    )
    return profiles
