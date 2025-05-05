from django import forms
from .models import Photo, ShortVideo, PhotoComment, ShortComment, Gift

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'visibility']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a caption...'}),
            'visibility': forms.Select(attrs={'class': 'form-select'})
        }

class ShortVideoForm(forms.ModelForm):
    class Meta:
        model = ShortVideo
        fields = ['video', 'thumbnail', 'caption', 'visibility']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a caption...'}),
            'visibility': forms.Select(attrs={'class': 'form-select'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = PhotoComment 
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Add a comment...'})
        }

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['name', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Gift name'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price'}),
        } 