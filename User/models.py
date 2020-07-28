from django.db import models
from django.contrib.auth.models import User
from DjangoDRF import choice
from django.db.models.signals import post_save
from django.dispatch import receiver


class Server(models.Model):
    plan_id = models.CharField(max_length=15, null=False, default='P101')
    ram = models.CharField(max_length=10, null=True)
    hdd = models.CharField(max_length=15, null=True)
    hosting_os = models.CharField(max_length=20, choices=choice.OS_CHOICE, default="window")
    price = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "tbl_servers"

        indexes = [
            models.Index( fields=['plan_id', ] ),
            models.Index( fields=['hosting_os', ] ),
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    first_name = models.CharField(max_length=140, null=True, blank=True)
    last_name = models.CharField( max_length=140, null=True, blank=True )
    city = models.CharField(max_length=140, null=True, blank=True)
    country = models.CharField(max_length=140, null=True, blank=True)

    @property
    def get_user_profile(self):
        return f"{self.city}, {self.country}"


@receiver(post_save, sender=User)
def setup_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    post_title = models.CharField(max_length=20, null=False)
    post_text = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = "tbl_post"


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    comment = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = "tbl_comments"



class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']

    def __str__(self):
        return self.headline


class Assignment(models.Model):
    user = models.CharField(max_length=10, default='amit')
    practice_duration = models.IntegerField(default=0)
    day = models.DateField()

    class Meta:
        db_table = "tbl_assigment"
