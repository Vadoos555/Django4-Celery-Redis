from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Sport, TagPost
from .forms import AddPostForm
from .utils import DataMixin
from .tasks import show_task1, add, multiply, mult_3


class SportHome(DataMixin, ListView):
    template_name = 'sport_site/index.html'
    context_object_name = 'posts'
    title_page = 'Main page'
    cat_selected = 0
    
    def get_queryset(self):
        return Sport.published.all().select_related('cat')
            

@login_required
def about(request):
    contact_list = Sport.published.all()
    paginator = Paginator(contact_list, 3)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'sport_site/about.html', {'title': 'About site', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'sport_site/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)
    
    def get_object(self, queryset=None):
        return get_object_or_404(Sport.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'sport_site/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Adding page'
    permission_required = 'sport_site.add_sport'
    
    def form_valid(self, form):
        sp = form.save(commit=False)
        sp.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Sport
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'sport_site/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Edit page'
    permission_required = 'sport_site.change_sport'


@permission_required(perm='sport_site.view_sport', raise_exception=True)
def feedback(request):
    
    show_task1.delay()
    add.delay(100, 200)
    multiply.delay(10, 55)
    mult_3.delay(5, 10, 7)
    
    data = {
        'title': 'Contacts',
        'phone': '(044)555-5555',
        'email': 'vadim@sport_site.com',
        'address': 'Ukraine, Kyiv, str. Main 55'
    }
    return render(request, 'sport_site/feedback.html', data)


def login(request):
    return HttpResponse('Authorization')


class SportCategory(DataMixin, ListView):
    template_name = 'sport_site/index.html'
    context_object_name = 'posts'
    allow_empty = False
    
    def get_queryset(self):
        return Sport.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title=f'Category - {cat.name}', cat_selected=cat.pk)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found...</h1>')


class TagPostList(DataMixin, ListView):
    template_name = 'sport_site/index.html'
    context_object_name = 'posts'
    allow_empty = False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f'Tag {tag.tag}')
    
    def get_queryset(self):
        return Sport.published.filter(tag__slug=self.kwargs['tag_slug']).select_related('cat')
    