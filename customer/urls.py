from django.urls import path
from . import views

urlpatterns = [
    path("complete-signup/", views.complete_sign_up, name="complete_sign_up"),
]
