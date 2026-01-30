from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Categories(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    description = models.TextField('Описание', blank=True)
    main_project = models.BooleanField(default=False)
    is_country = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('Заголовок', max_length=300)
    slug = models.SlugField('URL', max_length=300, unique=True, blank=True)
    content = CKEditor5Field('Содержание', config_name='extends')
    date = models.DateTimeField('Дата публикации', blank=True, null=True)
    categories = models.ManyToManyField(Categories, verbose_name='Категории', related_name='news')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    @property
    def comments_count(self):
        return self.comments.count()

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    content = models.TextField()
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-date']
