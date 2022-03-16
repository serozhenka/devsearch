import uuid
import math
from django.conf import settings
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
        ordering = ['-vote_ratio', '-vote_total', '-title']

    @property
    def image_url(self):
        try:
            url = self.featured_image.url
        except:
            url = f"{settings.MEDIA_URL}images/default.jpg"
        return url

    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()
        self.vote_total = total_votes
        self.vote_ratio = math.ceil(up_votes / total_votes * 100)
        self.save()

        return self

    def get_reviewers(self):
        return self.review_set.all().values_list('owner__id', flat=True)


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Upvote'),
        ('down', 'Downvote')
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    value = models.CharField(max_length=256, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner', 'project']]

class Tag(models.Model):
    name = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


