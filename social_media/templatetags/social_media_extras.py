from django import template
from social_media.models import Photo, ShortVideo

register = template.Library()

@register.filter
def get_model_name(obj):
    if isinstance(obj, Photo):
        return 'Photo'
    elif isinstance(obj, ShortVideo):
        return 'ShortVideo'
    return '' 