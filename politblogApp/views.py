from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, "content/home.html")

def category_view(request):
    return render(request, "content/article.html")
