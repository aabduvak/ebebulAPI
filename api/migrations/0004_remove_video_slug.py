# Generated by Django 4.1.7 on 2023-02-24 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_video_slug_alter_video_name_alter_video_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='slug',
        ),
    ]