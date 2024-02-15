from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'
    verbose_name = 'Рассылка'


class DjangoApschedulerConfig(AppConfig):
    name = "django_apscheduler"
    verbose_name = "Django APScheduler"
