from django.db import models

# Create your models here.
class Categories(models.Model):
    category = models.CharField(max_length=100)


    def __str__(self):
        return self.category

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, related_name='news')


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
