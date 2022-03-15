import uuid
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=128, null=True)
    name = models.CharField(max_length=128, null=True)
    email = models.EmailField(max_length=256, null=True)
    headline = models.CharField(max_length=256, null=True, blank=True)
    location = models.CharField(max_length=128, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(default='profile_images/default.png', upload_to='profile_images/', null=True, blank=True)

    social_github = models.CharField(max_length=256, null=True, blank=True)
    social_twitter = models.CharField(max_length=256, null=True, blank=True)
    social_linkedin = models.CharField(max_length=256, null=True, blank=True)
    social_stackoverflow = models.CharField(max_length=256, null=True, blank=True)
    social_website = models.CharField(max_length=256, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    subject = models.CharField(max_length=128, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject if self.subject else self.body[0:50]

    class Meta:
        ordering = ['is_read', '-created']

