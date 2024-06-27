from django import template
import avito.views as views
import avito.models as models

register = template.Library()

# @register.simple_tag(name= 'cats')
# def get_categories():
#     return views.cats_db

@register.simple_tag
def get_menu():
    return views.menu

@register.inclusion_tag('avito/list_categories.html')
def show_categories():
    cats = [(cat[0], cat[1]) for cat in models.Post.CAT]  # Используйте кортежи (slug, название на русском)
    return {'cats': cats}