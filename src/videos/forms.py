from django import forms
from .models import Video, Comment, Playlist

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail', 'category', 'is_short']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'is_short': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        } 