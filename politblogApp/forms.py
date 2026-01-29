from django import forms
from .models import News, Categories, Comments

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"
        labels = {
            "news_id": "News Id",
            "title": "Title",
            "content": "Content",
            "date": "Date",
            "author": "Author",
            "category": "Category",
        }
        widgets = {
            'news_id': forms.NumberInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'content': forms.TextInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'author': forms.TextInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'category': forms.TextInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = "__all__"
        labels = {
            "category": "Category",
        }
        widgets = {
            'category': forms.TextInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = "__all__"
        labels = {
            "comment_id": "Comment Id",
            "article_id": "Article Id",
            "name": "Name",
            "content": "Content",
            "website": "Website",
            "topic": "Topic",
            "date": "Date",
        }
        widgets = {
            'comment_id': forms.NumberInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'article_id': forms.NumberInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'content': forms.TextInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'website': forms.TextInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'placeholder': 'e.g 1', 'class': 'form-control'}),
        }