from django.db import models
from django.conf import settings
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post')
    
    def __str__(self):
        return f'Post (PK: {self.pk}, Author: {self.author.username})'

    class Meta:
        ordering = ['-pk']


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()

    def __str__(self):
        return f'Comment (PK: {self.pk}, Author: {self.author.username})'


    class Meta:
        ordering = ['-pk']