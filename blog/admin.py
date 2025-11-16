from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_at')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        """Admin action to approve pending posts."""
        from django.utils import timezone
        updated = 0
        for post in queryset.filter(status='pending'):
            post.status = 'published'
            post.published_at = timezone.now()
            post.save()
            updated += 1
        self.message_user(request, f'{updated} post(s) have been approved and published.')
    
    approve_posts.short_description = "Approve selected pending posts"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'approved')
    list_filter = ('approved',)
