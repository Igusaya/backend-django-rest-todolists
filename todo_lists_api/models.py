from django.db import models

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Card(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=False)
    position = models.SmallIntegerField()
    color = models.CharField(max_length=7, blank=True, default='#FFFFFF')
    owner = models.ForeignKey('auth.User', related_name='todo_lists_api', on_delete=models.CASCADE)

    class Meta:
        ordering = ['position', 'created']

    def save(self, *arg, **kwargs):
        super(Card, self).save(*arg, **kwargs)


class Profile(models.Model):
    # OneToOneField 1対1のリレーションを貼る
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    modify = models.DateTimeField(auto_now=True)
    #image = models.ImageField(upload_to='profIcon/', default='profIcon/defo.png')
    image = models.CharField(max_length=100, default='/image/profIcon/defo.png')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


"""
blank: フォームからの投稿時の必須条件（False：必須)
null: DB登録時の必須条件（False：必須)
"""
