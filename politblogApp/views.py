from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import NewsForm, CommentForm, CategoryForm
from .models import News, Comments, Categories
from django.db.models import Q


# about us
def about_us(request):
    categories = Categories.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'content/about_us.html', context)

# ----- FOR NEWS -----
def home_view(request):
    news_list = reversed(News.objects.all())
    categories = Categories.objects.all()

    context = {
        'news_list': news_list,
        'categories': categories
    }

    return render(request, 'content/home.html', context)

def news_detail_view(request, slug):
    news = get_object_or_404(News, slug=slug)

    related_posts = News.objects.filter(
        categories__in=news.categories.all(),
    ).exclude(id=news.id).distinct()[:4]

    form = CommentForm()

    context = {
        'news': news,
        'related_posts': related_posts,
        'categories': Categories.objects.all(),
        'form': form
    }
    return render(request, 'content/article.html', context)


# search
def search_news_view(request):
    query = request.GET.get('q')  # Получаем текст из инпута с именем 'q'
    results = []
    if query:
        # Ищем совпадения в заголовке ИЛИ в контенте (игнорируя регистр)
        results = reversed(News).objects.filter(
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

# comments
def add_comment(request, id):
    article = get_object_or_404(News, id=id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('news_detail', slug=article.slug)
    return redirect('news_detail', slug=article.slug)








# admin
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_dashboard(request):
    """Панель управления для администратора"""
    context = {
        'total_news': News.objects.count(),
        'total_categories': Categories.objects.count(),
        'categories': Categories.objects.all(),
    }
    return render(request, 'admin/dashboard.html', context)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Проверяем, что это именно админ (is_staff)
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard') # Название вашего пути в urls.py
    else:
        form = AuthenticationForm()
    return render(request, "admin/login.html", {"form": form})

# for news
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def create_news_view(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES) # Добавь request.FILES для картинок
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Новость успешно создана!")
                return redirect('create_news')
            except:
                # Эта ошибка поймает дубликат slug
                messages.error(request, "Ошибка: Новость с таким заголовком уже существует (дубликат slug).")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")

    context = {
        'form': form,
        'categories': Categories.objects.all(),
        'title': 'Создать новость',
    }
    return render(request, 'admin/news_form.html', context)
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_news_edit(request, pk):
    news = get_object_or_404(reversed(News), pk=pk)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Новость обновлена!")
                return redirect('news_detail', slug=news.slug)
            except:
                messages.error(request, "Не удалось сохранить: такой slug уже занят другой новостью.")
    else:
        form = NewsForm(instance=news)

    context = {
        'form': form,
        'news': news,
        'title': 'Редактировать новость',
        'categories': Categories.objects.all(),
    }
    return render(request, 'admin/news_form.html', context)
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_news_delete(request, pk):
    """Удаление новости"""
    news = get_object_or_404(reversed(News), pk=pk)

    if request.method == 'POST':
        news.delete()
        return redirect('home')


# ----- FOR CATEGORIES -----
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_categories(request):
    """Страница управления категориями и тегами"""
    categories = Categories.objects.all().prefetch_related('news')

    context = {
        'categories': categories,
    }
    return render(request, 'admin/categories.html', context)
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_category_create(request):
    """Создание категории"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        main_project = request.POST.get('main_project')
        is_country = request.POST.get('is_country')

        if main_project == 'on':
            main_project = True
        else:
            main_project = False
        if is_country == 'on':
            is_country = True
        else:
            is_country = False

        if not name:
            messages.error(request, 'Название категории не может быть пустым!')
            return redirect('admin_categories')
        if Categories.objects.filter(name__iexact=name).exists():
            messages.error(request, f'Категория с названием "{name}" уже существует!')
            return redirect('admin_categories')

        try:
            Categories.objects.create(
                name=name,
                description=description,
                main_project=main_project,
                is_country=is_country
            )
            messages.success(request, f'Категория "{name}" успешно создана!')
        except Exception as e:
            messages.error(request, f'Ошибка при создании категории: {str(e)}')

    return redirect('admin_categories')
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_category_quick_add(request):
    """Быстрое создание категории"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()

        if not name:
            messages.error(request, 'Введите название категории!')
            return redirect('admin_categories')
        if Categories.objects.filter(name__iexact=name).exists():
            messages.error(request, f'Категория "{name}" уже существует!')
            return redirect('admin_categories')

        try:
            Categories.objects.create(name=name)
            messages.success(request, f'Категория "{name}" добавлена!')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')

    return redirect('admin_categories')
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_category_edit(request, pk):
    """Редактирование категории"""
    categories = get_object_or_404(Categories, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        main_project = request.POST.get('main_project')
        is_country = request.POST.get('is_country')

        # Проверка на пустое имя
        if not name:
            messages.error(request, 'Название категории не может быть пустым!')
            return redirect('admin_categories')

        # Проверяем, не занято ли имя другой категорией (исключая текущую)
        if Categories.objects.filter(name__iexact=name).exclude(pk=pk).exists():
            messages.error(request, f'Категория с названием "{name}" уже существует!')
            return redirect('admin_categories')

        # Обновляем категорию
        try:
            categories.name = name
            categories.description = description
            categories.main_project = (main_project == 'on')
            categories.is_country = (is_country == 'on')
            categories.save()
            messages.success(request, f'Категория "{categories.name}" обновлена!')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении: {str(e)}')

    return redirect('admin_categories')
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_category_delete(request, pk):
    """Удаление категории"""
    categories = get_object_or_404(Categories, pk=pk)

    if request.method == 'POST':
        name = categories.name
        try:
            categories.delete()
            messages.success(request, f'Категория "{name}" удалена!')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении: {str(e)}')

    return redirect('admin_categories')
