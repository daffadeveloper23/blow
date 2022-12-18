from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Content)
admin.site.register(LikePost)
admin.site.register(FollowersCount)