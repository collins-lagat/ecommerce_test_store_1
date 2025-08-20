from django.urls import include, path
from rest_framework import routers

from orders import views

router = routers.DefaultRouter()

router.register(r"", views.CartViewSet)
router.register(r"item", views.CartItemViewSet)

urlpatterns = [
    path("api/cart/", include(router.urls)),
]
