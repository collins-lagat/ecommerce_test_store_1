from django.shortcuts import render

from products.models import Category


def index(request):
    categories = Category.objects.filter(parent=None)
    return render(request, "index.html", {"categories": categories})
