from django.db import models
from django.contrib.auth.models import User

class MoonPhase(models.Model):
    date = models.DateField()
    illumination_percentage = models.FloatField()

    def __str__(self):
        return f"Moon Phase on {self.date}"


class Constellation(models.Model):
    name = models.CharField(max_length=100)
    min_latitude = models.FloatField()
    max_latitude = models.FloatField()

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()

    def __str__(self):
        return self.name


class AstronomyEvent(models.Model):
    summary = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    # class Meta:
    #     db_table = 'login'  # 指定新的表名

    def __str__(self):
        return self.summary

class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='forum_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class ForumFavorite(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} favorites {self.post.title}"

from django.db import models


# 新建文件夹/meteor_app/models.py
class MeteorShower(models.Model):
    name = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)
    maximum_date = models.DateTimeField()
    maximum_lambda = models.FloatField()
    radiant_ra = models.FloatField()
    radiant_dec = models.FloatField()
    velocity = models.FloatField()
    r_value = models.FloatField()
    zhr = models.IntegerField()

    def __str__(self):
        return self.name