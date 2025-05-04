from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    class Meta:
        abstract = True

class Photo(Post):
    image = models.ImageField(upload_to='photos/')
    
    def __str__(self):
        return f"Photo by {self.user.username}"

class ShortVideo(Post):
    video = models.FileField(upload_to='shorts/')
    thumbnail = models.ImageField(upload_to='shorts/thumbnails/', blank=True)
    duration = models.DurationField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Short by {self.user.username}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        abstract = True

class PhotoComment(Comment):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f"Comment by {self.user.username} on photo {self.photo.id}"

class ShortComment(Comment):
    short = models.ForeignKey(ShortVideo, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f"Comment by {self.user.username} on short {self.short.id}"

class Gift(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='gifts/')
    
    def __str__(self):
        return self.name

class GiftTransaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_gifts')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_gifts')
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='gifts')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.sender.username} gifted {self.gift.name} to {self.receiver.username}"
