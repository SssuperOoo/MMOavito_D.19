from django import template

register = template.Library()

@register.filter
def get_category_display(cat_dict, category):
    return cat_dict.get(category, category)