from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import NewsForm, CommentForm, CategoryForm
from .models import News, Comments, Categories
from django.db.models import Q


#----- FOR NEWS -----
def home_view(request):
    return render(request, 'content/home.html')


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

    return render(request, 'content/home.html', {
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
def category_view(request, category_new, category_parent):
    # 1. Находим текущую категорию по её названию (поле category в модели Categories)
    # Если категория не найдена, вернется 404
    current_category = get_object_or_404(Categories, category=category_new)

    # 2. Получаем все новости, которые относятся к этой категории
    news = News.objects.filter(category=current_category)

    # 3. Находим родительскую категорию
    parent_cat = get_object_or_404(Categories, category=category_parent)

    if request.method == 'POST':
        # Здесь будет логика обработки POST, если нужно
        pass
    context = {
        'news': news,
        'current_category': current_category,
        'parent_category': parent_cat,
    }

    return render(request, 'category_detail.html', context)




def search_news(request):
    query = request.GET.get('q') # Получаем текст из инпута с именем 'q'
    results = []
    if query:
        # Ищем совпадения в заголовке ИЛИ в контенте (игнорируя регистр)
        results = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    return render(request, 'search_results.html', {
        'results': results,
        'query': query
    })
# <form action="{% url 'search_news' %}" method="get">
#     <input type="text" name="q" placeholder="Поиск новостей..." value="{{ request.GET.q }}">
#     <button type="submit">Найти</button>
# </form>
# <h1>Результаты поиска по запросу: "{{ query }}"</h1>
#
# {% if results %}
#     {% for item in results %}
#         <div>
#             <h3>{{ item.title }}</h3>
#             <p>{{ item.content|truncatewords:20 }}</p>
#             <a href="#">Читать полностью</a>
#         </div>
#         <hr>
#     {% endfor %}
# {% else %}
#     <p>Ничего не найдено. Попробуйте другой запрос.</p>
# {% endif %}