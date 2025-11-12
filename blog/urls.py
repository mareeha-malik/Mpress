from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('page/<int:page>/', views.HomeView.as_view(), name='home_paged'),
    # Specific post actions must come before the generic slug route
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/like/', views.post_like, name='post_like'),
    path('post/<slug:slug>/like/ajax/', views.post_like_ajax, name='post_like_ajax'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', views.TagListView.as_view(), name='tag_posts'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
