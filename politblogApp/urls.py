from django.urls import path
from . import views

# urls.py
urlpatterns = [
    path('', views.home_view, name='home'),
    # path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    # и т.д.
]