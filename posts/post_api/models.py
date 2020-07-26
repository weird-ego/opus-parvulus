from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256, unique=True)
    creation_date = models.DateField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    author_name = models.CharField(max_length=256)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=256)
    content = models.TextField()
    creation_date = models.DateField(auto_now_add=True)


class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["user", "post"]]
        indexes = [models.Index(fields=["user", "post"])]
