from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/profile/', null=True, blank=True)
    user_bio = models.TextField(max_length=500, null=True, blank=True)
    contact_number = models.IntegerField(default=0, null=True, blank=True)
    facebook_link = models.CharField(max_length=200, null=True, blank=True)
    instagram_link = models.CharField(max_length=200, null=True, blank=True)
    twitter_link = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)