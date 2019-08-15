from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    address = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return self.username

    def __repr__(self):
        return f"{self.__class__.__name__}(username:{self.username})"
