from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .forms import *
from .models import *
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all()
    return render(request, 'index.html', {
        'user_profile': user_profile,
        'posts': posts
    })

@login_required(login_url='signin')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            first = request.POST['first']
            last = request.POST['last']
            email = request.POST['email']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.first_name = first
            user_profile.last_name = last
            user_profile.email = email
            user_profile.save()
            
            
        else:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            first = request.POST['first']
            last = request.POST['last']
            email = request.POST['email']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.first_name = first
            user_profile.last_name = last
            user_profile.email = email
            user_profile.save()
            
        return redirect('setting')
    return render(request, 'setting.html', {
        'user_profile': user_profile
    })

def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Try Another Username')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Try Another Email')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                user.save()
                
                #log user in and redirect to setting page
                auth.login(request, auth.authenticate(username=username, password=password))
                
                
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                messages.info(request, 'Sign Up Success')
                return redirect('setting')
        else:
            messages.info(request, 'Password Not Match')
            return redirect('signup')

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user != None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Credential Invalid")
            return redirect('signin')
 
@login_required(login_url='signin')       
def signout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')    
def wiki(request, id):
    current_profile = Profile.objects.get(id_user=id)
    my_book = Book.objects.filter(book_author=request.user)
    return render(request, "wiki.html", {
        'current_profile': current_profile,
        'books': my_book
    })
    
@login_required(login_url='signin')
def make_book(request):
    if request.method == "GET":
        all_category = Category.objects.all()
        current_profile = Profile.objects.get(user=request.user)
        return render(request, "make_book.html", {
            "categories": all_category,
            'current_profile': current_profile
        })
    else:
        current_profile = Profile.objects.get(user=request.user)
        title = request.POST['title']
        description = request.POST['description']
        raw_cat = request.POST['category']
        category = Category.objects.get(category_name=raw_cat)
        author = request.user
        
        new_book = Book.objects.create(book_title=title, book_description=description, book_category=category, book_author=author)
        new_book.save()

        return redirect('make_book')
    
@login_required(login_url='signin')
def book_content(request, name):
    current_book = Book.objects.get(book_title=name)
    book_contents = Content.objects.filter(book=current_book)
    current_profile = Profile.objects.get(user=request.user)
    return render(request, "book_content.html", {
        'book': current_book,
        'contens': book_contents,
        'current_profile': current_profile
    })

@login_required(login_url='signin')   
def content_read(request, content):
    current_content = Content.objects.get(title=content)
    current_profile = Profile.objects.get(user=request.user)
    return render(request, "read_content.html", {
        "current_profile": current_profile,
        "content": current_content
    })

@login_required(login_url='signin')  
def make_content(request, title):
    current_profile = Profile.objects.get(user=request.user)
    current_book = Book.objects.get(book_title=title)
    if request.method == "POST":
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        new_content = Content.objects.all().last()
        new_content.book = current_book
        new_content.save()

        return HttpResponseRedirect('/')
    else:
        form = ContentForm
    return render(request, "make_content.html", {
        'form': form,
        'current_profile': current_profile,
        'current_book': current_book,
    })


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
    
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk
    
    if FollowersCount.objects.filter(follower=follower, user=user):
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
        
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')