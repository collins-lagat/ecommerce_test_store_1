from django.urls import include, path

from products import views


urlpatterns = [
    path("category/<int:category_id>/", views.category, name="category"),
    path("product/<int:product_id>/", views.product, name="product"),
    path("api/", include(views.router.urls)),
]
