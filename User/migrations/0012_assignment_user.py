# Generated by Django 2.2.1 on 2020-07-17 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_assignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='user',
            field=models.CharField(default='amit', max_length=10),
        ),
    ]
