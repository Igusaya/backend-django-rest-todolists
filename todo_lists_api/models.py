from django.db import models


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
