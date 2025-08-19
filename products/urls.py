from django.urls import path

from products import views


urlpatterns = [
    path("category/<int:category_id>/", views.category, name="category"),
    path("product/<int:product_id>/", views.product, name="product"),
]
