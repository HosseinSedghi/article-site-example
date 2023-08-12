from django import template
from jalali_date import datetime2jalali


register = template.Library()


@register.filter(name='jalali_date')
def jalali_date(date):
    return datetime2jalali(date).strftime('%Y/%m/%d')


@register.filter(name='jalali_time')
def jalali_time(time):
    return datetime2jalali(time).strftime('%H:%M:%S')