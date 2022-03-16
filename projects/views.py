from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from . import utils

def projectsHome(request):
    projects = utils.searchProjects(request)
    projects, paginator, custom_range = utils.paginateProjects(request, projects, results=6)

    return render(request, 'projects/projects.html', context={
        'projects': projects,
        'paginator': paginator,
        'custom_range': custom_range,
    })

def project(request, pk):
    projectObj = Project.objects.get(id=pk)

    if request.method == "GET":
        form = ReviewForm()
        return render(request, 'projects/single-project.html', context={'project': projectObj, 'form': form})
    elif request.method == "POST":
        try:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.owner = request.user.profile
                review.project = projectObj
                review.save()

                projectObj.get_vote_count()
                messages.success(request, 'Review successfully submitted')

        except IntegrityError:
            messages.error(request, 'Every user can create only one review per project')

        return redirect('project', pk=pk)

@login_required(login_url='login')
def create_project(request):
    if request.method == "GET":
        form = ProjectForm()
        return render(request, 'projects/project_form.html', context={'form': form})

    elif request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        new_tags = request.POST.get('new_tags').replace(',', '').split()

        if form.is_valid():
            projectObj = form.save(commit=False)
            projectObj.owner = request.user.profile
            projectObj.save()

            for tag in new_tags:
                if not Tag.objects.filter(name__iexact=tag):
                    tagObj = Tag.objects.create(name=tag)
                else:
                    tagObj = Tag.objects.get(name__iexact=tag)
                projectObj.tags.add(tagObj)

            return redirect('project', form.instance.id)

@login_required(login_url='login')
def update_project(request, pk):
    projectObj = Project.objects.get(id=pk)
    if request.user.profile != projectObj.owner:
        return HttpResponse('<h1>You are not allowed to update someone\'s project</h1>')

    if request.method == "GET":
        form = ProjectForm(instance=projectObj)
        return render(request, 'projects/project_form.html', context={'form': form, 'project': projectObj})
    elif request.method == "POST":
        new_tags = request.POST.get('new_tags').replace(',', '').split()

        form = ProjectForm(request.POST, request.FILES, instance=projectObj)
        if form.is_valid():
            form.save()
            for tag in new_tags:
                if not Tag.objects.filter(name__iexact=tag):
                    tagObj = Tag.objects.create(name=tag)
                else:
                    tagObj = Tag.objects.get(name__iexact=tag)
                projectObj.tags.add(tagObj)

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