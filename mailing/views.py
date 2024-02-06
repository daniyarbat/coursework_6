import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from blog.models import Article
from mailing.forms import SendingForm, SendingManagerForm

from mailing.models import Sending, Client, Logs
from mailing.templates.services import set_period


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
    template_name = 'mailing/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['object'])
        return context


class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    form_class = SendingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.options_owner = self.request.user
        send_params.next_try = set_period()
        send_params.save()

        return super().form_valid(form)


class SendingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        send_params = form.save()
        self.model.send_status = send_params.send_status
        send_params.next_try = set_period()
        send_params.save()

        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset

    def get_form_class(self):
        if self.request.user.groups.filter(name='manager'):
            return SendingManagerForm
        return SendingForm


class SendingDeleteView(LoginRequiredMixin, DeleteView):
    model = Sending
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
