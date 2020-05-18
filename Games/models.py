from django.db import models


class Games(models.Model):
    name = models.CharField(max_length=50, null=True)
    game_url = models.CharField(max_length=300, null=True)
    image_url = models.CharField(max_length=300, null=True)
    category = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "tbl_games"


class ContactUs(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=100, null=False)
    subject = models.CharField(max_length=100, null=False)
    message = models.CharField(max_length=300, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_contact_us"