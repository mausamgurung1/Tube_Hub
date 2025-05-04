from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.VideoFeedView.as_view(), name='video_feed'),
    path('shorts/', views.ShortVideoFeedView.as_view(), name='shorts_feed'),
    path('upload/', views.VideoUploadView.as_view(), name='upload'),
    path('video/<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('video/<int:video_id>/like/', views.like_video, name='like_video'),
    path('video/<int:video_id>/comment/', views.add_comment, name='add_comment'),
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('playlists/', views.PlaylistView.as_view(), name='playlists'),
] 