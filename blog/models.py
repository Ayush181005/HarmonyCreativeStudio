from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    views = models.IntegerField(default=0)
    title = models.CharField(max_length=500)
    content = models.TextField()
    keywords = models.CharField(default="", max_length=600, help_text="Seperate by Comma and space (', ')")
    author = models.CharField(max_length=225)
    slug = models.CharField(max_length=130)
    timeStamp = models.DateTimeField()
    featureImage = models.ImageField(upload_to="blog/images")
    uniqueVisitorIPs = models.TextField(default="", blank=True)
    metaDesc = models.CharField(max_length=200, help_text="min: 130 letters, max: 170 letters")

    def __str__(self):
        return self.title + ', by ' + self.author

    def get_absolute_url(self):
        return f'/blog/{self.slug}'

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comments = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default = now)

    def __str__(self):
        return self.comments[:30] + "... by " + self.user.username