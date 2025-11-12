from .models import Category, Tag, Post


def sidebar_data(request):
    return {
        'sidebar_categories': Category.objects.all()[:8],
        'sidebar_tags': Tag.objects.all()[:30],
        'sidebar_recent': Post.objects.filter(status='published').order_by('-published_at')[:5],
    }
