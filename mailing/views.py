from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from mailing.models import Sending


class BaseTemplateView(TemplateView):
    template_name = 'mailing/index.html'


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager'):
            queryset = queryset.all()
        else:
            queryset = queryset.filter(sending_owner=self.request.user)
        return queryset
