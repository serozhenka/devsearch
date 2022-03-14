from .models import Tag, Project
from django.db.models import Q

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
