from django.db import models
from django.utils.text import slugify


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta(object):
        db_table = "tbl_publisher"
        ordering = ["id"]

    def __str__(self):
        return self.name


class PostSearch(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    slug = models.SlugField(default='', blank=True)

    class Meta( object ):
        db_table = "tbl_post_search"
        # ordering = ["id"]

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(PostSearch, self).save()

    def __str__(self):
        return self.title
