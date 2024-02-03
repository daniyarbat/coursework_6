from django.db import models
from pytils.translit import slugify

from config import settings


NULLABLE = {
    'null': True, 'blank': True
}


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='url')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog_img/', **NULLABLE, verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('title', 'created_at', 'is_published',)
