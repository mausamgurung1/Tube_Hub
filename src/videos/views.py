from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Video, Comment, UserProfile, Playlist
from .forms import VideoUploadForm, CommentForm

# Create your views here.

class VideoFeedView(ListView):
    model = Video
    template_name = 'videos/feed.html'
    context_object_name = 'videos'
    paginate_by = 10

    def get_queryset(self):
        return Video.objects.all().order_by('-created_at')

class ShortVideoFeedView(ListView):
    model = Video
    template_name = 'videos/shorts_feed.html'
    context_object_name = 'videos'
    paginate_by = 10

    def get_queryset(self):
        return Video.objects.filter(is_short=True).order_by('-created_at')

class VideoDetailView(DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context

class VideoUploadView(LoginRequiredMixin, CreateView):
    model = Video
    form_class = VideoUploadForm
    template_name = 'videos/upload.html'
    success_url = reverse_lazy('video_feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.likes.all():
        video.likes.remove(request.user)
        liked = False
    else:
        video.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': video.likes.count()})

@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.user = request.user
            comment.save()
            return JsonResponse({
                'success': True,
                'comment': {
                    'content': comment.content,
                    'username': comment.user.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
    return JsonResponse({'success': False})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    user_profile = request.user.userprofile
    if user_to_follow in user_profile.following.all():
        user_profile.following.remove(user_to_follow)
        followed = False
    else:
        user_profile.following.add(user_to_follow)
        followed = True
    return JsonResponse({'followed': followed})

class PlaylistView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'videos/playlists.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)
