from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import BaseTemplateView, SendingListView, SendingCreateView, SendingUpdateView, SendingDeleteView, SendingDetailView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='home'),
    path('mailing_list/', SendingListView.as_view(), name='mailing_list'),
    path('create_mailing/', SendingCreateView.as_view(), name='create_mailing'),
    path('edit_mailing/<int:pk>', SendingUpdateView.as_view(), name='edit_mailing'),
    path('delete_mailing/<int:pk>', SendingDeleteView.as_view(), name='delete_mailing'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('update_message/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
]
