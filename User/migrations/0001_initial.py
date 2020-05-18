# Generated by Django 2.2.1 on 2020-04-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_id', models.CharField(max_length=15, null=True)),
                ('ram', models.CharField(max_length=10, null=True)),
                ('hdd', models.CharField(max_length=15, null=True)),
                ('hosting_os', models.CharField(max_length=20, null=True)),
                ('price', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'tbl_servers',
            },
        ),
    ]
