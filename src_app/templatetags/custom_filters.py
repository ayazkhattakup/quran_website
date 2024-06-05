from django import template

register = template.Library()

@register.filter
def format_duration(value):
    minutes, seconds = divmod(value, 60)
    return f'{minutes:02}:{seconds:02}'
