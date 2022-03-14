from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from . import utils

def projectsHome(request):
    projects = utils.searchProjects(request)
    projects, paginator, custom_range = utils.paginateProjects(request, projects, results=5)

    return render(request, 'projects/projects.html', context={
        'projects': projects,
        'paginator': paginator,
        'custom_range': custom_range,
    })

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', context={'project': projectObj})

@login_required(login_url='login')
def create_project(request):
    if request.method == "GET":
        form = ProjectForm()
        return render(request, 'projects/project_form.html', context={'form': form})

    elif request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            projectObj = form.save(commit=False)
            projectObj.owner = request.user.profile
            projectObj.save()

            return redirect('project', form.instance.id)

@login_required(login_url='login')
def update_project(request, pk):
    projectObj = Project.objects.get(id=pk)
    if request.user.profile != projectObj.owner:
        return HttpResponse('<h1>You are not allowed to update someone\'s project</h1>')

    if request.method == "GET":
        form = ProjectForm(instance=projectObj)
        return render(request, 'projects/project_form.html', context={'form': form})
    elif request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect('project', projectObj.id)

@login_required(login_url='login')
def delete_project(request, pk):
    projectObj = Project.objects.get(id=pk)
    if request.user.profile != projectObj.owner:
        return HttpResponse('<h1>You are not allowed to delete someone\'s project</h1>')

    if request.method == "GET":
        return render(request, 'delete_template.html', context={'obj': projectObj})
    elif request.method == "POST":
        projectObj.delete()
        return redirect('projects-home')