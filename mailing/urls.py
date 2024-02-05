from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import BaseTemplateView

app_name = MailingConfig.name

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='home'),
]
