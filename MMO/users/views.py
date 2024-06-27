from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, ActivationForm
from users.models import ActivationCode

User = get_user_model()

def activate_account(request, code):
    if request.method == 'POST':
        form = ActivationForm(request.POST)
        if form.is_valid():
            activation_code = get_object_or_404(ActivationCode, code=form.cleaned_data['code'])
            user = activation_code.user
            user.is_active = True
            user.save()
            activation_code.delete()
            return redirect('home')
    else:
        form = ActivationForm()
    return render(request, 'users/activate_account.html', {'form': form})
class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title' : 'Авторизация'}



class RegisterUserCreateView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile')
    def get_object(self, queryset=None):
        return self.request.user