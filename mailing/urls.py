from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import BaseTemplateView, SendingListView, SendingCreateView, SendingUpdateView, SendingDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, ClientListView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, LogsListView, UsersListView, UsersUpdateView

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

    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('edit_client/<int:pk>', ClientUpdateView.as_view(), name='edit_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),

    path('logs/', LogsListView.as_view(), name='logs'),
    path('users_table/', UsersListView.as_view(), name='users_table'),
    path('edit_user/<int:pk>', UsersUpdateView.as_view(), name='edit_user'),
]
