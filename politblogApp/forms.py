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
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок новости'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Полный текст новости'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'categories': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['image'].required = False
        self.fields['date'].required = True

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'description', 'main_project']
        labels = {
            "category": "Category",
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название категории'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание категории (необязательно)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['image'].required = False
        self.fields['main_project'].required = True

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
