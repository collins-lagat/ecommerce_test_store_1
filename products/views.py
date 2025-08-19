from django.shortcuts import get_object_or_404, render

from products.models import Category, Product


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = category.get_all_products()
    return render(
        request, "category-single.html", {"category": category, "products": products}
    )


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "product-single.html", {"product": product})
