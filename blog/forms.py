from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'content', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-white/90 border border-white/30 text-gray-800', 'placeholder': 'Post title'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl bg-white/90 border border-white/30 text-gray-800'}),
            'tags': forms.SelectMultiple(attrs={'class': 'w-full px-4 py-2 rounded-xl bg-white/90 border border-white/30 text-gray-800', 'size': 5}),
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-white/90 border border-white/30 text-gray-800', 'rows': 10, 'placeholder': 'Write your post here...'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'block w-full text-sm text-gray-600'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'rows': 3})}
