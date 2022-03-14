import uuid
from django.db import models
from users.models import Profile

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(default='project_images/default.jpg', null=True, blank=True, upload_to='project_images')
    demo_link = models.CharField(max_length=512, null=True, blank=True)
    source_link = models.CharField(max_length=512, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Upvote'),
        ('down', 'Downvote')
    )

    # owner =
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    value = models.CharField(max_length=256, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

