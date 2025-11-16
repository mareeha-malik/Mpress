from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Tag
from .forms import CommentForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import Group


class HomeView(View):
    def get(self, request):
        q = request.GET.get('q')
        posts = Post.objects.filter(status='published')
        if q:
            posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
        paginator = Paginator(posts, 6)
        page = request.GET.get('page')
        posts_page = paginator.get_page(page)
        categories = Category.objects.all()[:6]
        tags = Tag.objects.all()[:20]
        recent = Post.objects.filter(status='published')[:5]
        return render(request, 'blog/home.html', {'posts': posts_page, 'categories': categories, 'tags': tags, 'recent': recent, 'q': q})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comment_form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user if request.user.is_authenticated else None
            comment.save()
            return redirect(post.get_absolute_url())
    # determine whether the current user already liked this post
    liked_by_user = False
    if request.user.is_authenticated:
        liked_by_user = post.likes.filter(user=request.user).exists()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form, 'liked_by_user': liked_by_user})


def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    if not request.user.is_authenticated:
        return redirect('login')
    like, created = post.likes.get_or_create(user=request.user)
    if not created:
        # user already liked -> remove
        like.delete()
    return redirect(post.get_absolute_url())


from django.http import JsonResponse


def post_like_ajax(request, slug):
    """AJAX endpoint to toggle like and return JSON with new count."""
    post = get_object_or_404(Post, slug=slug, status='published')
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login_required'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'error': 'invalid_method'}, status=405)
    like, created = post.likes.get_or_create(user=request.user)
    liked = created
    if not created:
        like.delete()
        liked = False
    return JsonResponse({'liked': liked, 'count': post.likes.count()})


class CategoryListView(View):
    def get(self, request, slug):
        cat = get_object_or_404(Category, slug=slug)
        posts = Post.objects.filter(category=cat, status='published')
        paginator = Paginator(posts, 6)
        page = request.GET.get('page')
        posts_page = paginator.get_page(page)
        return render(request, 'blog/list.html', {'posts': posts_page, 'title': f'Category: {cat.name}'})


class TagListView(View):
    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tags=tag, status='published')
        paginator = Paginator(posts, 6)
        page = request.GET.get('page')
        posts_page = paginator.get_page(page)
        return render(request, 'blog/list.html', {'posts': posts_page, 'title': f'Tag: {tag.name}'})


class SearchView(View):
    def get(self, request):
        q = request.GET.get('q')
        posts = Post.objects.filter(status='published')
        if q:
            posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
        paginator = Paginator(posts, 6)
        page = request.GET.get('page')
        posts_page = paginator.get_page(page)
        return render(request, 'blog/list.html', {'posts': posts_page, 'title': f'Search: {q}'})


class GroupRequiredMixin(UserPassesTestMixin):
    """Require that the user is in the 'Author' group or is staff."""
    def test_func(self):
        user = getattr(self.request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        return user.is_staff or user.groups.filter(name='Author').exists()


class DashboardView(LoginRequiredMixin, GroupRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.filter(author=request.user)
        return render(request, 'blog/dashboard.html', {'posts': posts})



class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user or self.request.user.is_staff


class PostCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Force new posts to always be pending
        form.instance.status = 'pending'
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
