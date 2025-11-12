# Helper to create sample data via Django shell
# Run with: python manage.py shell < manage_sample_data.py
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post

# Create admin user if not exists
u, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
if created:
    u.set_password('password')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    # Ensure admin is in Author group
from django.contrib.auth.models import Group
group, _ = Group.objects.get_or_create(name='Author')
if not u.groups.filter(name='Author').exists():
    u.groups.add(group)

cats = ['Lifestyle','Inspiration','Tech','Travel']
for c in cats:
    Category.objects.get_or_create(name=c)

tags = ['design','life','tutorial','travel','coding']
for t in tags:
    Tag.objects.get_or_create(name=t)

import random
from django.utils import timezone

for i in range(8):
    cat = Category.objects.order_by('?').first()
    post = Post.objects.create(title=f'Sample Post {i+1}', content='Lorem ipsum dolor sit amet ...'*5, author=u, category=cat, status='published', published_at=timezone.now())
    post.tags.set(Tag.objects.order_by('?')[:2])
    post.save()

print('Sample data created')
