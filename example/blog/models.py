from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    author = models.ForeignKey(User)
    title = models.TextField()
    body = models.TextField()
    tags = models.ManyToManyField('Tag')

    class Meta:
        verbose_name_plural = "entries"

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name