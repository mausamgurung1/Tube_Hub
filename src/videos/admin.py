from django.contrib import admin
from .models import UserProfile, Video, Comment, Playlist

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'bio')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'views', 'created_at', 'is_short')
    list_filter = ('category', 'is_short', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'video__title')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    filter_horizontal = ('videos',)
