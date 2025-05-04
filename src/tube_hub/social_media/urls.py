from django.urls import path
from . import views

app_name = 'social_media'

urlpatterns = [
    path('photos/', views.photo_feed, name='photo_feed'),
    path('photos/upload/', views.upload_photo, name='upload_photo'),
    path('photos/<int:post_id>/comment/', views.add_comment, {'post_type': 'photo'}, name='add_photo_comment'),
    path('photos/<int:post_id>/like/', views.like_post, {'post_type': 'photo'}, name='like_photo'),
    path('photos/<int:post_id>/gift/', views.send_gift, {'post_type': 'photo'}, name='send_photo_gift'),
    path('photos/<int:post_id>/delete/', views.delete_post, {'post_type': 'photo'}, name='delete_photo'),
    
    path('shorts/', views.shorts_feed, name='shorts_feed'),
    path('shorts/upload/', views.upload_short, name='upload_short'),
    path('shorts/<int:post_id>/comment/', views.add_comment, {'post_type': 'short'}, name='add_short_comment'),
    path('shorts/<int:post_id>/like/', views.like_post, {'post_type': 'short'}, name='like_short'),
    path('shorts/<int:post_id>/gift/', views.send_gift, {'post_type': 'short'}, name='send_short_gift'),
    path('shorts/<int:post_id>/delete/', views.delete_post, {'post_type': 'short'}, name='delete_short'),
] 