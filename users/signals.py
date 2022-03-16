from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        send_mail(
            subject='Registration to devsearch successful',
            message=
            f'''
            We are glad to see you here, {profile.username}!
            Wish you have the best experience out here!
            ''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[profile.email],
            fail_silently=False,
        )

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    if not created:
        profile = instance
        user = profile.user

        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()