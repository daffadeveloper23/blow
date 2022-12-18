from importlib.resources import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('setting', views.setting, name="setting"),
    path('upload', views.upload, name="upload"),
    path('follow', views.follow, name="follow"),
    path('profile/<str:pk>', views.profile, name="profile"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('wiki/<int:id>', views.wiki, name="wiki"),
    path('make_book', views.make_book, name="make_book"),
    path('book_content/<str:name>', views.book_content, name="book_content"),
    path('like_post', views.like_post, name="like_post"),
    path('content_read/<str:content>', views.content_read, name="content_read"),
    path('make_content/<str:title>', views.make_content, name="make_content")
]