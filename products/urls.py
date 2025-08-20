from django.urls import include, path
from rest_framework import routers

from products import views

router = routers.DefaultRouter()

router.register(r"category", views.CategoryViewSet)
router.register(r"product", views.ProductViewSet)

urlpatterns = [
    path("category/<int:category_id>/", views.category, name="category"),
    path("product/<int:product_id>/", views.product, name="product"),
    path("api/", include(router.urls)),
]
