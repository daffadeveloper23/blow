from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from ckeditor.fields import RichTextField

User = get_user_model()
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user
    
class Category(models.Model):
    category_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.category_name
    
class Book(models.Model):
    book_title = models.CharField(max_length=100)
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    book_author = models.ForeignKey(User, on_delete=models.CASCADE)
    book_description = models.CharField(max_length=1000, blank=True)
    
    def __str__(self):
        return self.book_title
    
class Content(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    text = RichTextField(blank=True, null=True)
    author = models.CharField(max_length=50)
    video = models.FileField(upload_to='content_videos', blank=True)
    
    def __str__(self):
        return f"{self.title} on {self.book}"
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.username} like on {self.post_id}"
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length=1000)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user