from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    """Model definition for User."""

    GENERE_CHOICES = (
        ("M","Masculino"),
        ("F","Femenino"),
        ("O","Otros"),
    )

    # TODO: Define fields here
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    names = models.CharField(max_length=30, blank=True, default="")
    last_names = models.CharField(max_length=30, blank=True, default="")
    genere = models.CharField(max_length=1, choices=GENERE_CHOICES, blank=True)
    is_staff = models.BooleanField(default=False)
    

    USERNAME_FIELD = "username"
    
    REQUIRED_FIELDS = ["email",]

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return f"{self.names} {self.last_names}"

    class Meta:
        """Meta definition for User."""

        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_full_name()

