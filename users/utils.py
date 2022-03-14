from .models import Skill, Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProfiles(request):
    user_query = request.GET.get('user_query') if request.GET.get('user_query') else ''
    projects = Profile.objects.distinct().filter(
        Q(name__icontains=user_query) |
        Q(username__icontains=user_query) |
        Q(headline__icontains=user_query) |
        Q(location__icontains=user_query) |
        Q(skill__in=Skill.objects.filter(name__icontains=user_query))
    )
    return projects

def paginateProfiles(request, profiles, results):
    paginator = Paginator(profiles, results)
    page = int(request.GET.get('page')) if request.GET.get('page') else 1

    try:
        paginator.page(page)
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page = paginator.num_pages

    profiles = paginator.page(page)

    leftIndex = (page - 4) if (page - 4) >= 1 else 1
    rightIndex = (page + 4) if (page + 4) <= paginator.num_pages else paginator.num_pages
    custom_range = range(leftIndex, rightIndex + 1)

    return profiles, paginator, custom_range