from django.contrib import admin

from mailing.models import Sending, Client, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email',)
    list_filter = ('client_name',)
    search_fields = ('client_name',)


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'send_name', 'send_start', 'send_finish', 'send_period', 'send_status')
    list_filter = ('send_status',)
    search_fields = ('send_status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text',)
    list_filter = ('title',)
    search_fields = ('title',)
