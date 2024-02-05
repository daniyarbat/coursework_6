import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from blog.models import Article
from mailing.forms import SendingForm

from mailing.models import Sending, Client, Logs


class BaseTemplateView(TemplateView):
    template_name = 'mailing/index.html'
    extra_context = {'title': 'Рассылки'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['full_list'] = Sending.objects.all().count()
        context_data['active_list'] = Sending.objects.filter(is_active=True).count()
        context_data['unique_clients_list'] = Client.objects.all().count()
        blog_list = list(Article.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        context_data['clients_count'] = len(Client.objects.all())
        return context_data


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager'):
            queryset = queryset.all()
        else:
            queryset = queryset.filter(sending_owner=self.request.user)
        return queryset


class SendingDetailView(DetailView):
    model = Sending

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['object'])
        return context


class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.options_owner = self.request.user
        # send_params.next_try = set_period()
        send_params.save()

        return super().form_valid(form)


class SendingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy ( 'mailing:mailing_list' )


class SendingDeleteView(LoginRequiredMixin, DeleteView):
    model = Sending
    success_url = reverse_lazy('mailing:mailing_list')





