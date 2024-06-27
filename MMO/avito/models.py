from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, blank=True)
    CAT = (('tanks', 'Танки'),
           ('healers', 'Хилы'),
           ('damage_dealers', 'ДД'),
           ('dealers', 'Торговцы'),
           ('gildmasters', 'Гилдмастеры'),
           ('quest_givers', 'Квестгиверы'),
           ('blacksmiths', 'Кузнецы'),
           ('tanners', 'Кожевники'),
           ('potion_makers', 'Зельевары'),
           ('spell_masters', 'Мастера заклинаний'))
    category = models.CharField(max_length=15, choices=CAT, verbose_name='Категория')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата объявления')
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Фото')
    files = RichTextUploadingField(verbose_name='Дополнительные файлы', default='', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # Используем unidecode для нормализации заголовка
            self.slug = slugify(unidecode(self.title))
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super(Post, self).save(*args, **kwargs)
        # self.send_notification_to_all_users()  # Здесь у меня происходит рассылка всем пользователям касательно добавления новой статьи, выключил с целью не получать
        # ошибки связанные с SMTPDataError: (554, b'5.7.1 Message rejected under suspicion of SPAM')

    def send_notification_to_all_users(self):
        User = get_user_model()
        recipient_list = User.objects.values_list('email', flat=True)
        subject = 'Новое объявление на сайте'
        message = f'Добавлено новое объявление: {self.title}\nКатегория: {self.get_category_display()}\nОписание: {self.text}\nСсылка: {settings.DOMAIN_NAME}{self.get_absolute_url()}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)

    class Meta:
        verbose_name = 'Объявления'
        verbose_name_plural = 'Объявления'
        ordering = ['-create_date']
        indexes = [
            models.Index(fields=['-create_date'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def get_delete_url(self):
        return reverse('deletepost', kwargs={'post_slug': self.slug})

    def get_edit_url(self):
        return reverse('editpost', kwargs={'post_slug': self.slug})


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    status = models.BooleanField(default=False)
    text = models.TextField(verbose_name='Текст')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[0:50]

    class Meta:
        verbose_name = 'Отклики'
        verbose_name_plural = 'Отклики'
        ordering = ['status']
        indexes = [
            models.Index(fields=['status'])
        ]
