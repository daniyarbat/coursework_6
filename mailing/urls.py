from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import BaseTemplateView, SendingListView, SendingCreateView, SendingUpdateView, SendingDeleteView, SendingDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='home'),
    path('mailing_list/', SendingListView.as_view(), name='mailing_list'),
    path('mailing_view/<int:pk>', SendingDetailView.as_view(), name='mailing_view'),
    path('create_mailing/', SendingCreateView.as_view(), name='create_mailing'),
    path('edit_mailing/<int:pk>', SendingUpdateView.as_view(), name='edit_mailing'),
    path('delete_mailing/<int:pk>', SendingDeleteView.as_view(), name='delete_mailing'),
]
