from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('news/', views.news_list_view, name='news_list'),
    path('category/<int:cat_id>/', views.news_list_view, name='news_by_category'),
    path('create/', views.create_news_view, name='create_news'),
]