from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Photo, ShortVideo, PhotoComment, ShortComment, Gift, GiftTransaction
from .forms import PhotoForm, ShortVideoForm, CommentForm, GiftForm

# Create your views here.

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
def add_comment(request, post_type, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            
            if post_type == 'photo':
                photo = get_object_or_404(Photo, id=post_id)
                comment.photo = photo
            else:
                short = get_object_or_404(ShortVideo, id=post_id)
                comment.short = short
            
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
def like_post(request, post_type, post_id):
    if post_type == 'photo':
        post = get_object_or_404(Photo, id=post_id)
    else:
        post = get_object_or_404(ShortVideo, id=post_id)
    
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
def send_gift(request, post_type, post_id):
    if request.method == 'POST':
        form = GiftForm(request.POST)
        if form.is_valid():
            gift = form.cleaned_data['gift']
            if post_type == 'photo':
                post = get_object_or_404(Photo, id=post_id)
            else:
                post = get_object_or_404(ShortVideo, id=post_id)
            
            transaction = GiftTransaction.objects.create(
                sender=request.user,
                receiver=post.user,
                gift=gift,
                post=post
            )
            
            return JsonResponse({
                'success': True,
                'gift': {
                    'name': gift.name,
                    'image': gift.image.url
                }
            })
    return JsonResponse({'success': False})

@login_required
def delete_post(request, post_type, post_id):
    if post_type == 'photo':
        post = get_object_or_404(Photo, id=post_id)
    else:
        post = get_object_or_404(ShortVideo, id=post_id)
    
    if post.user == request.user:
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    else:
        messages.error(request, 'You are not authorized to delete this post.')
    
    if post_type == 'photo':
        return redirect('social_media:photo_feed')
    else:
        return redirect('social_media:shorts_feed')
