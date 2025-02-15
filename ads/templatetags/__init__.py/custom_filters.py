from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Возвращает значение по ключу в словаре, если ключ не найден - возвращает 0"""
    return dictionary.get(key, 0)