from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe

from .models import Sport, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Status of sportsmen'
    parameter_name = 'status'
    
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('married', 'Married'),
            ('single', 'Unmarried'),
        ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == 'married':
            return queryset.filter(soulmate__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(soulmate__isnull=True)


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'post_photo', 'photo', 'content', 'cat', 'soulmate', 'tag']
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ['tag']
    readonly_fields = ['post_photo']
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 7
    actions = ['set_published', "set_draft"]
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter,'cat__name', 'is_published']
    
    @admin.display(description='Picture')
    def post_photo(self, sport: Sport):
        if sport.photo:
            return mark_safe(f"<img src='{sport.photo.url}' width=50>")
        return 'No photo'
    
    @admin.action(description='Publish selected records')
    def set_published(self, request, queryset):
        count = queryset.update(is_published = Sport.Status.PUBLISHED)
        self.message_user(request, f'Changed {count} records')
    
    @admin.action(description='Unpublish selected records')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published = Sport.Status.DRAFT)
        self.message_user(request, f'{count} records are unpublished', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['id']
