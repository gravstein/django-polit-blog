from django.shortcuts import render, redirect

# Create your views here.
from .forms import NewsForm, CommentForm, CategoryForm
from .models import News, Comments, Categories

#----- FOR NEWS -----
def home_view(request):
    return render(request, 'politblogApp/home.html')


def create_news_view(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('-----')
    return render(request, 'politblogApp/-----.html', {'form': form})


def news_list_view(request):
    category_id = request.GET.get('category')
    categories = Categories.objects.all()

    if category_id:
        news_s = News.objects.filter(category_id=category_id)
    else:
        news_s = News.objects.all()

    return render(request, 'politblogApp/-----.html', {
        'news_s': news_s,
        'categories': categories,
        'selected_category': category_id
    })


def news_update_view(request, news_id):
    news = News.objects.get(news_id=news_id)
    form = NewsForm(instance=news)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('-----')
    return render(request, 'politblogApp/-----.html', {'form': form})


def product_delete_view(request, news_id):
    news = News.objects.get(news_id=news_id)
    if request.method == 'POST':
        news.delete()
        return redirect('-----')
    return render(request, 'politblogApp/-----.html', {'news': news})


# ----- FOR CATEGORIES -----
# def category_view(request, category_new, category_parent):
#     news = News.objects.get(category=category_new)
#     categories = Categories.objects.get(category=category_parent)
#     if request.method == 'POST':
#      pass
