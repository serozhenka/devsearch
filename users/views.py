from django.shortcuts import render

def profilesPage(request):
    return render(request, 'users/profiles.html', context={})
