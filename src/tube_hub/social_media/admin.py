from django.contrib import admin
from .models import Photo, ShortVideo, PhotoComment, ShortComment, Gift, GiftTransaction

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'visibility')
    list_filter = ('visibility', 'created_at')
    search_fields = ('user__username', 'caption')

@admin.register(ShortVideo)
class ShortVideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'visibility', 'views')
    list_filter = ('visibility', 'created_at')
    search_fields = ('user__username', 'caption')

@admin.register(PhotoComment)
class PhotoCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'created_at')
    search_fields = ('user__username', 'content')

@admin.register(ShortComment)
class ShortCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'short', 'created_at')
    search_fields = ('user__username', 'content')

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(GiftTransaction)
class GiftTransactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'gift', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('sender__username', 'receiver__username', 'gift__name')
