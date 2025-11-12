from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import ProfileForm
from blog.models import Post


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Auto-assign to "Author" group so new users can create posts
            group, created = Group.objects.get_or_create(name='Author')
            user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = getattr(user, 'profile', None)
    posts = Post.objects.filter(author=user, status='published')
    return render(request, 'accounts/profile_detail.html', {'author': user, 'profile': profile, 'posts': posts})


@login_required
def profile_edit(request):
    profile = getattr(request.user, 'profile', None)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})
