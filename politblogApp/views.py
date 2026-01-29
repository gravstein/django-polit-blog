from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import NewsForm, CommentForm, CategoryForm
from .models import News, Comments, Categories
from django.db.models import Q


# Проверка на администратора
def is_admin(user):
    return user.is_staff or user.is_superuser


# ----- FOR NEWS -----
def home_view(request):
    news_list = News.objects.all()
    categories = Categories.objects.all()

    context = {
        'news_list': news_list,
        'categories': categories
    }

    return render(request, 'content/home.html', context)


def news_list_view(request):
    Categories_id = request.GET.get('Categories')
    categories = Categories.objects.all()

    if Categories_id:
        news_s = News.objects.filter(Categories_id=Categories_id)
    else:
        news_s = News.objects.all()

    return render(request, 'politblogApp/-----.html', {
        'news_s': news_s,
        'categories': categories,
        'selected_Categories': Categories_id
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


# search
def search_news_view(request):
    query = request.GET.get('q')  # Получаем текст из инпута с именем 'q'
    results = []
    if query:
        # Ищем совпадения в заголовке ИЛИ в контенте (игнорируя регистр)
        results = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    return render(request, 'content/home.html', {
        'news_list': results,
        #'query': query
    })

# category
def category_news_view(request, slug):
    """Показывает новости по выбранной категории"""
    # Получаем категорию по slug или возвращаем 404
    category = get_object_or_404(Categories, slug=slug)

    # Получаем все новости этой категории
    news_list = News.objects.filter(categories=category).order_by('-date')

    # Получаем все категории для sidebar
    categories = Categories.objects.all()

    context = {
        'news_list': news_list,
        'categories': categories,
        'current_category': category,  # для отображения названия категории
    }

    return render(request, 'content/home.html', context)



# admin
# @login_required
# @user_passes_test(is_admin)
def admin_dashboard(request):
    """Панель управления для администратора"""
    context = {
        'total_news': News.objects.count(),
        # 'published_news': News.objects.filter(status='published').count(),
        # 'draft_news': News.objects.filter(status='draft').count(),
        'total_categories': Categories.objects.count(),
        # 'total_tags': Tag.objects.count(),
        'recent_news': News.objects.all()[:5],
    }
    return render(request, 'admin/dashboard.html', context)


# @login_required
# @user_passes_test(is_admin)
def create_news_view(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'admin/news_form.html', {'form': form})


# ----- FOR CATEGORIES -----
# @login_required
# @user_passes_test(is_admin)
def admin_categories(request):
    """Страница управления категориями и тегами"""
    categories = Categories.objects.all().prefetch_related('news')

    context = {
        'categories': categories,
    }
    return render(request, 'admin/categories.html', context)


# @login_required
# @user_passes_test(is_admin)
def admin_category_create(request):
    """Создание категории"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        main_project = request.POST.get('main_project')

        if main_project == 'on':
            main_project = True
        else:
            main_project = False

        if name:
            Categories.objects.create(name=name, description=description, main_project=main_project)
            messages.success(request, f'Категория "{name}" успешно создана!')
        else:
            messages.error(request, 'Название категории обязательно!')

    return redirect('admin_categories')


# @login_required
# @user_passes_test(is_admin)
def admin_category_quick_add(request):
    """Быстрое создание категории"""
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            Categories.objects.create(name=name)
            messages.success(request, f'Категория "{name}" добавлена!')
        else:
            messages.error(request, 'Введите название категории!')

    return redirect('admin_categories')


# @login_required
# @user_passes_test(is_admin)
def admin_category_edit(request, pk):
    """Редактирование категории"""
    categories = get_object_or_404(Categories, pk=pk)

    main_project = request.POST.get('main_project')

    if main_project == 'on':
        categories.main_project = True
    else:
        categories.main_project = False

    if request.method == 'POST':
        categories.name = request.POST.get('name')
        categories.slug = request.POST.get('slug')
        categories.description = request.POST.get('description', '')
        categories.save()
        messages.success(request, f'Категория "{categories.name}" обновлена!')

    return redirect('admin_categories')


# @login_required
# @user_passes_test(is_admin)
def admin_category_delete(request, pk):
    """Удаление категории"""
    categories = get_object_or_404(Categories, pk=pk)

    if request.method == 'POST':
        name = categories.name
        categories.delete()
        messages.success(request, f'Категория "{name}" удалена!')

    return redirect('admin_categories')
