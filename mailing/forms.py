from datetime import datetime, timedelta

from django import forms
from django.utils import timezone

from mailing.models import Sending


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
        exclude = ('next_try', 'sending_owner', 'send_status',)


class SendingManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Sending
        fields = ('is_active',)
