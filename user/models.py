from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
ROLE_CHOICES = (
        (1, 'Manager'),
        (2, 'Vendeur'),
        (3,'Livreur'),
        (4,'Receiver'),
        (5, 'Picker')
    )
class User(AbstractUser):
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True)
    phone = models.CharField(max_length=25)

