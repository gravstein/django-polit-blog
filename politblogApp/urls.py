from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home'),
    path('news/<slug:slug>/', views.news_detail_view, name='news_detail'),
    path('category/<slug:slug>/', views.category_news_view, name='category_news'),
    path('search', views.search_news_view, name='search_news'),
    path('comment/<int:id>/', views.add_comment, name='add_comment'),
    path('about-us/', views.about_us, name='about_us'),

    # admin
    path('create/', views.create_news_view, name='create_news'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('news/<int:pk>/edit/', views.admin_news_edit, name='admin_news_edit'),
    path('news/<int:pk>/delete/', views.admin_news_delete, name='admin_news_delete'),

    # Категории
    path('categories/', views.admin_categories, name='admin_categories'),
    path('categories/create/', views.admin_category_create, name='admin_category_create'),
    path('categories/quick-add/', views.admin_category_quick_add, name='admin_category_quick_add'),
    path('categories/<int:pk>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path('categories/<int:pk>/delete/', views.admin_category_delete, name='admin_category_delete'),
]

