from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'social_media'

def redirect_to_home(request):
    return redirect('social_media:home_feed')

urlpatterns = [
    # Home feed and authentication
    path('', views.home_feed, name='home_feed'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    
    # Profile
    path('profile/<str:username>/', views.profile, name='profile'),
    
    # Photo related URLs
    path('photos/', views.photo_feed, name='photo_feed'),
    path('photos/upload/', views.upload_photo, name='upload_photo'),
    path('photos/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photos/<int:photo_id>/delete/', views.delete_post, name='delete_photo'),
    
    # Shorts related URLs
    path('shorts/', views.shorts_feed, name='shorts_feed'),
    path('shorts/upload/', views.upload_short, name='upload_short'),
    path('shorts/<int:short_id>/', views.short_detail, name='short_detail'),
    path('shorts/<int:short_id>/delete/', views.delete_post, name='delete_short'),
    
    # Interaction URLs
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/gift/', views.send_gift, name='send_gift'),
] 