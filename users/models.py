from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'null': True, 'blank': True
}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    is_active = models.BooleanField(default=False, verbose_name='статус активности')
    email_verificator = models.CharField(max_length=50, **NULLABLE, verbose_name='код верификации почты')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ('is_active',)
