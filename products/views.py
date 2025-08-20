from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, routers, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = category.get_all_products()
    return render(
        request, "category-single.html", {"category": category, "products": products}
    )


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "product-single.html", {"product": product})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"])
    def average_price(self, request, pk=None):
        category = self.get_object()
        return Response({"average_price": category.average_price})


class ProductViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


router = routers.DefaultRouter()

router.register(r"category", CategoryViewSet)
router.register(r"product", ProductViewSet)
