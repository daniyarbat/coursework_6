from datetime import datetime, timedelta

from django import forms
from django.forms import DateTimeInput
from django.utils import timezone

from mailing.models import Sending, Message, Client
from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ['send_period', 'mail_title', 'client_email']:
                field.widget.attrs['class'] = 'form-select'
            elif field_name == 'is_active':
                field.widget.attrs['class'] = 'form'
            else:
                field.widget.attrs['class'] = 'form-control'


class SendingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Sending
        exclude = ('next_try', 'sending_owner', 'send_status')

        widgets = {
            'send_start': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
            'send_finish': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
        }


class SendingManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Sending
        fields = ('is_active',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('message_owner',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('client_owner',)


class UsersForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active',)
