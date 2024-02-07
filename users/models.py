import random

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'null': True, 'blank': True
}

random_code = str(random.randint(00000000, 99999999))


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    is_active = models.BooleanField(default=False, verbose_name='статус активности')
    verification_code = models.CharField(max_length=8, verbose_name='код подтверждения почты', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = str(random.randint(10000000, 99999999))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ('is_active',)
