from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} Profile'

class Video(models.Model):
    CATEGORY_CHOICES = [
        ('entertainment', 'Entertainment'),
        ('education', 'Education'),
        ('gaming', 'Gaming'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='video_likes', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_short = models.BooleanField(default=False)  # For TikTok-like short videos

    def __str__(self):
        return self.title

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.video.title}'

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    videos = models.ManyToManyField(Video, related_name='playlists', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
