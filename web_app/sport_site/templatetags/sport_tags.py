from django import template

from django.db.models import Count
from django.core.cache import cache

from sport_site.models import Category, TagPost
from sport_site.utils import menu



register = template.Library()


@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag('sport_site/list_cat.html')
def show_categories(cat_selected=0):
    cats = cache.get('cats')
    
    if not cats:
        cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
        cache.set('cats', cats, 60*10)
        
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('sport_site/list_tags.html')
def show_all_tags():
    tags = cache.get('tags')
    
    if not tags:
        tags = TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)
        cache.set('tags', tags, 60*10)
        
    return {'tags': tags}
