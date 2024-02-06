from django.db import models
from django.conf import settings
from django.utils import timezone

NULLABLE = {'null': True, 'blank': True}

PERIOD_CHOICES = (
    ('Ежедневно', 'Ежедневно'),
    ('Еженедельно', 'Еженедельно'),
    ('Ежемесячно', 'Ежемесячно')
)

STATUS_CHOICES = (
    ('Создана', 'Создана'),
    ('Запущена', 'Запущена'),
    ('Завершена', 'Завершена')
)


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='тема письма')
    text = models.TextField(verbose_name='текст письма')
    message_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Client(models.Model):
    client_email = models.CharField(max_length=150, verbose_name="контактный email", unique=True)
    client_name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)
    client_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь',
                                     on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.client_email} - {self.client_name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('client_name',)


class Sending(models.Model):
    send_name = models.CharField(max_length=200, verbose_name='наименование рассылки', default=None)
    send_start = models.DateTimeField(default=timezone.now, verbose_name='время начала рассылки')
    send_finish = models.DateTimeField(default=timezone.now, verbose_name='время окончания рассылки')
    next_try = models.DateTimeField(default=timezone.now, verbose_name='следующая попытка', **NULLABLE)
    send_period = models.CharField(max_length=20, verbose_name='периодичность', choices=PERIOD_CHOICES, default='')
    mail_title = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='тема рассылки', default=None)
    send_status = models.CharField(max_length=20, verbose_name='статус рассылки', choices=STATUS_CHOICES, default='Создана')
    client_email = models.ManyToManyField('Client', verbose_name="контактный email")
    sending_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.SET_NULL, **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активность')

    def __str__(self):
        return f"{self.send_name}"

    class Meta:
        verbose_name = 'настройка рассылки'
        verbose_name_plural = 'настройки рассылки'
        ordering = ('send_start',)


class Logs(models.Model):
    send_name = models.CharField(max_length=200, verbose_name='наименование рассылки', default=None)
    last_try = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='дата и время последней попытки')
    status_try = models.CharField(max_length=20, verbose_name='статус попытки')
    server_answer = models.TextField(verbose_name='ответ сервера', **NULLABLE, default='')
    logs_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.SET_NULL, **NULLABLE)
    send_email = models.EmailField(max_length=150, verbose_name='почта отправки', **NULLABLE)

    def __str__(self):
        return f"{self.status_try}: {self.last_try}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
        ordering = ('-last_try',)
