from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def add_days(date, days):
    return date + timedelta(days=days)
