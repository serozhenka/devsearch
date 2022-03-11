from django.urls import path
from . import views

urlpatterns = [
    path('', views.profilesPage, name='profiles'),
]
