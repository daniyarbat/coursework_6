import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from blog.models import Article
from mailing.forms import SendingForm, SendingManagerForm, MessageForm, ClientForm, UsersForm

from mailing.models import Sending, Client, Logs, Message
from mailing.services import set_period
from users.models import User


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
        return context_data


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset.all()
        else:
            if user.groups.filter(name='manager').exists():
                return queryset.all()
            else:
                return queryset.filter(sending_owner=user)


class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    form_class = SendingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.sending_owner = self.request.user or self.request.user.is_superuser
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


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(message_owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message_params = form.save()
        message_params.message_owner = self.request.user
        message_params.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client_owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.client_owner = self.request.user
        send_params.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(logs_owner=self.request.user)
        return queryset


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'mailing/users_list.html'


class UsersUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsersForm
    template_name = 'mailing/user_form.html'
    success_url = reverse_lazy('mailing:users_table')
