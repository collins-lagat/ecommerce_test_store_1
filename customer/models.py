from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, null=True)
