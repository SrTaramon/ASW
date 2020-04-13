from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


class Submit(models.Model):
    """
    Modelo que representa una submit
    """
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=100,blank=True)
    text = models.TextField(max_length=400,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField('date published', auto_now_add=True)
    likes = models.IntegerField(default=0)
    path = models.CharField(max_length=100,blank=True)
    qttcom = models.IntegerField(default=0)
    def __str__(self):

        return self.title

class Like(models.Model):
    post = models.ForeignKey('Submit', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    value = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now= True)

    def str(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")

class Comment(models.Model):
    submit = models.ForeignKey('Submit', on_delete=models.CASCADE, null=True)
    text = models.TextField(max_length=400)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField('date published', auto_now_add=True)

class Usuari(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        about = models.TextField(max_length=400,blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Usuari.objects.create(user=instance)
