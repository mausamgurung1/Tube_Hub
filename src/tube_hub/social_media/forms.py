from django import forms
from .models import Photo, ShortVideo, PhotoComment, ShortComment, Gift

class PhotoForm(forms.ModelForm):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_posts')
    likes = models.ManyToManyField(User, related_name='liked_photos')
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'visibility']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3}),
            'visibility': forms.Select(attrs={'class': 'form-select'})
        }

class ShortVideoForm(forms.ModelForm):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_posts')
    likes = models.ManyToManyField(User, related_name='liked_photos')
    class Meta:
        model = ShortVideo
        fields = ['video', 'thumbnail', 'caption', 'visibility']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3}),
            'visibility': forms.Select(attrs={'class': 'form-select'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = PhotoComment  # Base model for comments
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'})
        }

class GiftForm(forms.Form):
    gift = forms.ModelChoiceField(
        queryset=Gift.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    ) 