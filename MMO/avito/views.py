from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from avito.filters import MessageFilter
from avito.forms import AddPostForm, UploadFileForm, AddMessageForm
from avito.models import Post, Message

menu = [{'title': "Объявления", 'url_name': 'home'},
        {'title': "Добавить объявление", 'url_name': 'addpost'},
        {'title': "Ваши отклики", 'url_name': 'otklik'},
]

def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )


class PostListView(ListView):
    model = Post
    template_name = 'avito/index.html'
    context_object_name = 'posts'
    paginate_by = 5

class OtklikListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'avito/otklik.html'
    context_object_name = 'otklik'


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = MessageFilter(self.request.GET, queryset, user=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostCategoryListView(ListView):
    template_name = 'avito/index.html'
    context_object_name = 'posts'
    # allow_empty = False   #Вызывает ошибку 404 если таких категорий нет.
    paginate_by = 5
    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs['cat_slug'])  # self.kwargs['cat_slug'] содержит переменные поставляющиеся с маршрутом

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'avito/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class PostCreateView(LoginRequiredMixin,CreateView):
    form_class = AddPostForm
    model = Post
    template_name = 'avito/addpost.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Установка автора как текущего пользователя
        return super().form_valid(form)

class MessageCreateView(LoginRequiredMixin, CreateView):
    form_class = AddMessageForm
    model = Message
    template_name = 'avito/addpost.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Устанавливаем текущего пользователя как автора отклика
        post_slug = self.kwargs['post_slug']  # Получаем slug поста из URL
        post = get_object_or_404(Post, slug=post_slug)  # Получаем объект поста по его slug или ошибку 404
        form.instance.post = post  # Связываем отклик с соответствующим постом
        response = super().form_valid(form)

        # Отправка уведомления автору поста
        recipient_email = post.author.email
        subject = 'Новый отклик на ваше объявление'
        message = f'У вас новый отклик на ваше объявление "{post.title}".\nПосмотреть отклики можно по ссылке: http://127.0.0.1:8000/otklik/'
        send_notification_email(subject, message, [recipient_email])

        return response

class PostUpdateView(LoginRequiredMixin,UpdateView):

    form_class = AddPostForm
    model = Post
    template_name = 'avito/addpost.html'
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('home')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'avito/deletepost.html'
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('home')

def accept_otklik(request, pk):
    if request.user.is_authenticated:
        otklik = get_object_or_404(Message, pk=pk, post__author=request.user)
        otklik.status = True
        otklik.save()

        # Отправка уведомления автору отклика
        recipient_email = otklik.author.email
        subject = 'Ваш отклик был принят'
        message = f'Ваш отклик на объявление "{otklik.post.title}" был принят.'
        send_notification_email(subject, message, [recipient_email])

    return redirect('otklik')

# Удалить отклик
def delete_otklik(request, pk):
    if request.user.is_authenticated:
        otklik = get_object_or_404(Message, pk=pk, post__author=request.user)
        otklik.delete()
    return redirect('otklik')
