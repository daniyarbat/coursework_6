import random

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def logout_view(self, request):
        logout(request)
        return redirect(reverse_lazy('users:login'))


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    success_url = reverse_lazy('users:email_confirm_form')

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject='Подтверждение почты в Сервисе рассылок.',
            message=f'Вы зарегистрировались в Сервисе рассылок. Введите код в форму подтверждения - {user.verification_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class EmailConfirmView(View):
    model = User
    template_name = 'users/email_confirm_form.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        code = request.POST.get('ver_code')
        user = User.objects.filter(verification_code=code).first()

        if user is not None and user.verification_code == code:
            user.is_active = True
            user.save()
            return redirect('users:login')
        else:
            return redirect('users:email_confirm_form')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_pass = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Новый пароль на сайте',
        message=f'Ваш новый пароль - {new_pass}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_pass)
    request.user.save()
    return redirect(reverse('users:login'))
