from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import  forms
from django.core.exceptions import ValidationError

from .models import *

class AddPostForm(forms.ModelForm):
    files = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 20, 'rows': 10}), required=False)
    category = forms.ChoiceField(
        choices=[('', 'Категория не выбрана')] + list(Post.CAT),
        label='Категория'
    )

    title = forms.CharField(
        max_length=256,
        required=True,
        label= 'Название',
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 7}),
        required=True,
        label= 'Описание',
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    class Meta:
        model = Post
        fields = ['category', 'title', 'text', 'photo', 'files' ]
        widgets = {

        }
        labels = {'files': 'Видео',}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return title

class AddMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {}
        labels = {}


class UploadFileForm(forms.Form):
    file = forms.FileField(label='файл')

