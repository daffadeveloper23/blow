# Generated by Django 4.1.1 on 2022-12-16 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_pedia', '0006_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=1000)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]