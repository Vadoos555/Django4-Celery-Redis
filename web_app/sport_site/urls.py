from django.urls import path, register_converter
from django.views.decorators.cache import cache_page

from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('', cache_page(60*15)(views.SportHome.as_view()), name='home'),
    path('about/', views.about, name='about'),
    path('add_page', views.AddPage.as_view(), name='add_page'),
    path('feedback', views.feedback, name='feedback'),
    path('login', views.login, name='login'),
    path('post/<slug:post_slug>/', cache_page(60*5)(views.ShowPost.as_view()), name='post'),
    path('category/<slug:cat_slug>/', views.SportCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
]
