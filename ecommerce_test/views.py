from django.shortcuts import render

from orders.models import Order
from products.models import Category


def index(request):
    categories = Category.objects.filter(parent=None)
    return render(request, "index.html", {"categories": categories})


def profile(request):
    orders = Order.objects.filter(user=request.user, state="C").all()
    return render(request, "profile.html", {"orders": orders})
