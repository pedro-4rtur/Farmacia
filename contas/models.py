from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Cliente(AbstractUser):
    telefone = models.CharField(max_length=11)
    endereco = models.CharField()