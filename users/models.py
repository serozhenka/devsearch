from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    headline = models.CharField(max_length=256, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(default='profile_images/default.png', upload_to='profile_images/', null=True, blank=True)

    social_github = models.CharField(max_length=256, null=True, blank=True)
    social_twitter = models.CharField(max_length=256, null=True, blank=True)
    social_linkedin = models.CharField(max_length=256, null=True, blank=True)
    social_youtube = models.CharField(max_length=256, null=True, blank=True)
    social_website = models.CharField(max_length=256, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.username)
