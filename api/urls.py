from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('projects/', views.getProjects, name='projects'),
    path('projects/<str:pk>/', views.getProject, name='project'),
    path('projects/<str:pk>/vote/', views.projectVote, name='project-vote'),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]