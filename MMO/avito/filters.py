from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from .models import Message, Post


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class MessageFilter(FilterSet):
    post_title = ModelChoiceFilter(
        queryset=Post.objects.none(),  # Начальное значение queryset пусто
        field_name='post__title',
        label='Название объявления',
        to_field_name='title',
        empty_label='Выберите название',
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Обновляем queryset для выбора только объявлений пользователя
            self.filters['post_title'].queryset = Post.objects.filter(author=user)

    class Meta:
        model = Message
        fields = ['post_title']