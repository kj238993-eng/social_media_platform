from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from .models import UserProfile, Post, Comment, Like, Follow
import json

def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def feed_view(request):
    # Determine feed type (all vs following)
    feed_type = request.GET.get('feed', 'all')
    
    if feed_type == 'following':
        # Get list of user IDs that current user follows
        following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
        posts = Post.objects.filter(user_id__in=following_ids)
    else:
        posts = Post.objects.all()
    
    # Pre-check likes for the logged-in user to show filled heart icons
    liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
    
    # Get all users (except self) for "who to follow" suggestions
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))
    suggestions = User.objects.exclude(id=request.user.id).exclude(id__in=following_ids)[:5]
    
    context = {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'suggestions': suggestions,
        'feed_type': feed_type,
    }
    return render(request, 'core/feed.html', context)

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile
    posts = Post.objects.filter(user=profile_user)
    
    # Stats
    posts_count = posts.count()
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    
    # Check if logged in user is following this profile user
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    
    liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'posts_count': posts_count,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'liked_post_ids': liked_post_ids,
    }
    return render(request, 'core/profile.html', context)

@login_required
@require_POST
def create_post(request):
    content = request.POST.get('content', '').strip()
    image_url = request.POST.get('image_url', '').strip() or None
    
    if content:
        Post.objects.create(
            user=request.user,
            content=content,
            image_url=image_url
        )
    return redirect('feed')

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_qs = Like.objects.filter(user=request.user, post=post)
    
    if like_qs.exists():
        like_qs.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
        
    likes_count = post.likes.count()
    return JsonResponse({
        'liked': liked,
        'likes_count': likes_count
    })

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
    except json.JSONDecodeError:
        content = request.POST.get('content', '').strip()
        
    if not content:
        return JsonResponse({'error': 'Comment content cannot be empty'}, status=400)
        
    comment = Comment.objects.create(
        post=post,
        user=request.user,
        content=content
    )
    
    return JsonResponse({
        'comment_id': comment.id,
        'username': comment.user.username,
        'profile_picture_url': comment.user.profile.profile_picture_url or '',
        'content': comment.content,
        'created_at': comment.created_at.strftime('%b %d, %Y, %I:%M %p')
    })

@login_required
@require_POST
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        return JsonResponse({'error': 'You cannot follow yourself'}, status=400)
        
    follow_qs = Follow.objects.filter(follower=request.user, following=target_user)
    
    if follow_qs.exists():
        follow_qs.delete()
        following = False
    else:
        Follow.objects.create(follower=request.user, following=target_user)
        following = True
        
    followers_count = Follow.objects.filter(following=target_user).count()
    following_count = Follow.objects.filter(follower=target_user).count()
    
    return JsonResponse({
        'following': following,
        'followers_count': followers_count,
        'following_count': following_count
    })

@login_required
@require_POST
def edit_profile(request):
    bio = request.POST.get('bio', '').strip()
    profile_picture_url = request.POST.get('profile_picture_url', '').strip()
    
    profile = request.user.profile
    profile.bio = bio
    if profile_picture_url:
        profile.profile_picture_url = profile_picture_url
    profile.save()
    
    return redirect('profile', username=request.user.username)
