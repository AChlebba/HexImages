from django.db import models
from django.contrib.auth.models import AbstractUser



class Tier(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class CustomUser(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, default=None)



