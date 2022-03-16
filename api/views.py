from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},
        {'DELETE': '/api/projects/delete-tag'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serialized = ProjectSerializer(projects, many=True)
    return Response(serialized.data)

@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serialized = ProjectSerializer(project, many=False)
    return Response(serialized.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    profile = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=profile,
        project=project,
    )
    review.value = data.get('value')
    review.save()
    project.get_vote_count()

    serialized = ProjectSerializer(project, many=False)
    return Response(serialized.data)

@api_view(['DELETE'])
def deleteTag(request):
    tag_id = request.data.get('tag')
    project_id = request.data.get('project')

    project_obj = Project.objects.get(id=project_id)
    tag_obj = Tag.objects.get(id=tag_id)

    project_obj.tags.remove(tag_obj)
    return Response('Tag was deleted!')

