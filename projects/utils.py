from .models import Tag, Project
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProjects(request):
    project_query = request.GET.get('project_query') if request.GET.get('project_query') else ''
    projects = Project.objects.distinct().filter(
        Q(owner__name__icontains=project_query) |
        Q(owner__username__icontains=project_query) |
        Q(title__icontains=project_query) |
        Q(description__icontains=project_query) |
        Q(tags__in=Tag.objects.filter(name__icontains=project_query))
    )
    return projects

def paginateProjects(request, projects, results):
    paginator = Paginator(projects, results)
    page = int(request.GET.get('page')) if request.GET.get('page') else 1

    try:
        paginator.page(page)
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page = paginator.num_pages

    projects = paginator.page(page)

    leftIndex = (page - 4) if (page - 4) >= 1 else 1
    rightIndex = (page + 4) if (page + 4) <= paginator.num_pages else paginator.num_pages
    custom_range = range(leftIndex, rightIndex + 1)

    return projects, paginator, custom_range