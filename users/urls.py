from django.urls import path
from . import views

urlpatterns = [
    path('', views.profilesPage, name='profiles'),
    path('profiles/<str:pk>/', views.userProfile, name='user-profile'),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register")
]
