from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


# Create your models here.
class Categories(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    main_project = models.BooleanField(default=False)

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
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField('Дата публикации', blank=True, null=True)
    categories = models.ManyToManyField(Categories, verbose_name='Категории', related_name='news')

    def __str__(self):
        return self.title

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    article = models.ForeignKey(News, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField()
    website = models.URLField()
    topic = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
