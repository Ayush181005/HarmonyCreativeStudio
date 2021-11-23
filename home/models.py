from django.db import models
from django.utils.timezone import now
from django_resized import ResizedImageField

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    timeStamp = models.DateTimeField(default = now)

    def __str__(self):
        return self.content[:20] + '..., from ' + self.name

class Testimonial(models.Model):
    sno = models.AutoField(primary_key=True)
    nameAndDesignation = models.CharField(max_length=255)
    content = models.CharField(max_length=355)

    def __str__(self):
        return self.nameAndDesignation

class Portfolio(models.Model):
    sno = models.IntegerField(default=1)
    category = models.CharField(max_length=355)
    slug = models.CharField(max_length=100)
    desc = models.TextField()
    projectInfo = models.TextField()
    metaDesc = models.CharField(max_length=200, help_text="min: 130 letters, max: 170 letters")
    keywords = models.CharField(default="", max_length=600)
    featureImage = models.ImageField(upload_to="home/portfolio", blank=True)
    img1 = models.ImageField(upload_to="home/portfolio", help_text="300x300px")
    img2 = models.ImageField(upload_to="home/portfolio", blank=True, help_text="300x300px")
    img3 = models.ImageField(upload_to="home/portfolio", blank=True, help_text="300x300px")
    img4 = models.ImageField(upload_to="home/portfolio", blank=True, help_text="300x300px")
    img5 = models.ImageField(upload_to="home/portfolio", blank=True, help_text="300x300px")
    img6 = models.ImageField(upload_to="home/portfolio", blank=True, help_text="300x300px")
    img7 = models.ImageField(upload_to="home/portfolio", blank=True, help_text="300x300px")
    img8 = models.ImageField(upload_to="home/portfolio", blank=True, help_text="300x300px")
    img9 = models.ImageField(upload_to="home/portfolio", blank=True, help_text="300x300px")
    img10 = models.ImageField(upload_to="home/portfolio", blank=True, help_text="300x300px")

    def __str__(self):
        return str(self.sno) + ". " + self.category

    def get_absolute_url(self):
        return f'/portfolio/{self.slug}'    

class Client(models.Model):
    logo = models.ImageField(upload_to="home/clients")
    name = models.CharField(max_length=355)
    timeStamp = models.DateTimeField(default = now)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    sno = models.AutoField(primary_key=True)
    photo = ResizedImageField(upload_to="home/our_team", help_text="644x641px", size=[644, 641], crop=['middle', 'center'], force_format='PNG')
    name = models.CharField(max_length=400)
    designation = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class broadcasted_message(models.Model):
    msg = models.TextField()
    timeStamp = models.DateTimeField(default = now)
    activeDays = models.IntegerField(help_text="The no. of days for which the message should be shown.")

    def __str__(self):
        return self.msg[:15] + "..."