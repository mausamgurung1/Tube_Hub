from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Photo, ShortVideo, PhotoComment, ShortComment, Gift, TrendingTag, GiftTransaction
from .forms import PhotoForm, ShortVideoForm, CommentForm, GiftForm
from django.contrib.auth.forms import UserCreationForm

@login_required
def home_feed(request):
    # Get users that the current user follows
    following_users = User.objects.filter(followers__follower=request.user)
    
    # Get posts from followed users
    followed_photos = Photo.objects.filter(
        user__in=following_users,
        visibility='public'
    ).order_by('-created_at')
    
    followed_shorts = ShortVideo.objects.filter(
        user__in=following_users,
        visibility='public'
    ).order_by('-created_at')
    
    # Get suggested posts (posts from users that your followed users follow)
    suggested_users = User.objects.filter(
        followers__follower__in=following_users
    ).exclude(id=request.user.id).distinct()
    
    suggested_photos = Photo.objects.filter(
        user__in=suggested_users,
        visibility='public'
    ).exclude(user__in=following_users).order_by('-created_at')[:5]
    
    suggested_shorts = ShortVideo.objects.filter(
        user__in=suggested_users,
        visibility='public'
    ).exclude(user__in=following_users).order_by('-created_at')[:5]
    
    # Combine and sort followed posts by creation date
    followed_posts = list(followed_photos) + list(followed_shorts)
    followed_posts.sort(key=lambda x: x.created_at, reverse=True)
    
    # Combine and sort suggested posts by creation date
    suggested_posts = list(suggested_photos) + list(suggested_shorts)
    suggested_posts.sort(key=lambda x: x.created_at, reverse=True)
    
    # Get trending tags (top 5 by post count)
    trending_tags = TrendingTag.objects.order_by('-post_count')[:5]
    
    return render(request, 'social_media/home_feed.html', {
        'followed_posts': followed_posts,
        'suggested_posts': suggested_posts,
        'trending_tags': trending_tags,
        'following_count': following_users.count(),
    })

@login_required
def photo_feed(request):
    photos = Photo.objects.filter(visibility='public').order_by('-created_at')
    return render(request, 'social_media/photo_feed.html', {'photos': photos})

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('social_media:photo_feed')
    else:
        form = PhotoForm()
    return render(request, 'social_media/upload_photo.html', {'form': form})

@login_required
def shorts_feed(request):
    shorts = ShortVideo.objects.filter(visibility='public').order_by('-created_at')
    return render(request, 'social_media/shorts_feed.html', {'shorts': shorts})

@login_required
def upload_short(request):
    if request.method == 'POST':
        form = ShortVideoForm(request.POST, request.FILES)
        if form.is_valid():
            short = form.save(commit=False)
            short.user = request.user
            short.save()
            messages.success(request, 'Short video uploaded successfully!')
            return redirect('social_media:shorts_feed')
    else:
        form = ShortVideoForm()
    return render(request, 'social_media/upload_short.html', {'form': form})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            
            # Try to find the post (either photo or short)
            try:
                photo = Photo.objects.get(id=post_id)
                comment.photo = photo
            except Photo.DoesNotExist:
                try:
                    short = ShortVideo.objects.get(id=post_id)
                    comment.short = short
                except ShortVideo.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Post not found'})
            
            comment.save()
            return JsonResponse({
                'success': True,
                'comment': {
                    'user': comment.user.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
    return JsonResponse({'success': False})

@login_required
def like_post(request, post_id):
    # Try to find the post (either photo or short)
    try:
        post = Photo.objects.get(id=post_id)
    except Photo.DoesNotExist:
        try:
            post = ShortVideo.objects.get(id=post_id)
        except ShortVideo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'})
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': post.likes.count()
    })

@login_required
def send_gift(request, post_id):
    # Try to find the post (either photo or short)
    try:
        post = Photo.objects.get(id=post_id)
        post_type = 'photo'
    except Photo.DoesNotExist:
        try:
            post = ShortVideo.objects.get(id=post_id)
            post_type = 'short'
        except ShortVideo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'})
    
    if request.method == 'POST':
        form = GiftForm(request.POST, request.FILES)
        if form.is_valid():
            gift = form.save()
            transaction = GiftTransaction.objects.create(
                sender=request.user,
                receiver=post.user,
                gift=gift,
                photo=post if post_type == 'photo' else None,
                short=post if post_type == 'short' else None
            )
            messages.success(request, 'Gift sent successfully!')
            return redirect('social_media:home_feed')
    else:
        form = GiftForm()
    
    return render(request, 'social_media/send_gift.html', {
        'form': form,
        'post': post,
        'post_type': post_type
    })

@login_required
def delete_post(request, post_id):
    # Try to find the post (either photo or short)
    try:
        post = Photo.objects.get(id=post_id)
        post_type = 'photo'
    except Photo.DoesNotExist:
        try:
            post = ShortVideo.objects.get(id=post_id)
            post_type = 'short'
        except ShortVideo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'})
    
    if post.user == request.user:
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    else:
        messages.error(request, 'You are not authorized to delete this post.')
    
    if post_type == 'photo':
        return redirect('social_media:photo_feed')
    else:
        return redirect('social_media:shorts_feed')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('social_media:home_feed')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('social_media:home_feed')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('social_media:login')

@login_required
def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'social_media/photo_detail.html', {'photo': photo})

@login_required
def short_detail(request, short_id):
    short = get_object_or_404(ShortVideo, id=short_id)
    return render(request, 'social_media/short_detail.html', {'short': short})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    photos = Photo.objects.filter(user=user, visibility='public').order_by('-created_at')
    shorts = ShortVideo.objects.filter(user=user, visibility='public').order_by('-created_at')
    
    # Combine and sort by creation date
    all_posts = list(photos) + list(shorts)
    all_posts.sort(key=lambda x: x.created_at, reverse=True)
    
    return render(request, 'social_media/profile.html', {
        'profile_user': user,
        'posts': all_posts,
        'photos': photos,
        'shorts': shorts,
    }) 