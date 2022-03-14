from django.urls import path
from . import views

urlpatterns = [
    path('', views.profilesPage, name='profiles'),
    path('profiles/<str:pk>/', views.userProfile, name='user-profile'),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('account/', views.accountPage, name="account"),
    path('edit-account/', views.editAccountPage, name='edit-account'),

    path('create-skill/', views.create_skill, name='create-skill'),
    path('update-skill/<str:pk>/', views.update_skill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete-skill'),
]
