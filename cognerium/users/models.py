from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from rest_framework.authtoken.models import Token
from menu.models import CogneriumAbstractModel

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin, CogneriumAbstractModel):
    remarks = models.TextField(null=True, blank=True)
    profilepic = models.ImageField(
        upload_to='images/', max_length=100, null=True)
    ismanager = models.BooleanField(default=False)
    first_name = models.CharField(max_length=15, default='')
    last_name = models.CharField(max_length=20, default='')
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(('staff status'), default=False, help_text=(
        'Designates whether the user can log into this admin site.'))
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'ismanager', 'is_active']
    password_reset_salt = models.IntegerField(blank=True, null=True)
    objects = UserManager()

    def get_full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username or self.email

    def get_short_name(self):
        """Return the email."""
        return self.email or self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        Token.objects.get_or_create(user=self)

    def __str__(self):
        return self.get_full_name()
