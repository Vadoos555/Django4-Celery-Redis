from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.contrib.auth import get_user_model


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=Sport.Status.PUBLISHED)


class Sport(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'draft'
        PUBLISHED = 1, 'published'
    
    title = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Photo')
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISHED, verbose_name='status')
    
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='category')
    tag = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='tags')
    soulmate = models.OneToOneField('Soulmate', on_delete=models.SET_NULL, null=True, 
                                    blank=True, related_name='soul_mate', verbose_name='soulmate')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)
    
    objects = models.Manager()
    published = PublishedManager()
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'famous sportsmen'
        verbose_name_plural = 'famous sportsmen'
        
        ordering = ['time_create']
        indexes = [
            models.Index(fields=['-time_create']), 
            ]
    
    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})
    

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='category')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    
    def __str__(self) -> str:
        return self.tag
    
    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})


class Soulmate(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    w_count = models.IntegerField(blank=True, default=0)
    
    def __str__(self):
        return self.name
