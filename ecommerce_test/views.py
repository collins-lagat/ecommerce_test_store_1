from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render

from orders.models import Order
from products.models import Category


def index(request):
    categories = Category.objects.filter(parent=None)
    return render(request, "index.html", {"categories": categories})


def logout(request):
    if not request.user.is_authenticated:
        return redirect("/")

    auth_logout(request)
    return redirect("/")


def profile(request):
    orders = Order.objects.filter(user=request.user, state="C").all()
    return render(request, "profile.html", {"orders": orders})
