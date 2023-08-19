from django import template
from jalali_date import datetime2jalali
import humanize
import datetime as dt

register = template.Library()


@register.filter(name='jalali_date')
def jalali_date(date):
    return datetime2jalali(date).strftime('%Y/%m/%d')


@register.filter(name='jalali_date_humanize')
def jalali_date_humanize(date):
    _t = humanize.i18n.activate("fa_IR")
    return humanize.naturaltime(date, minimum_unit='microseconds')

@register.filter(name='filter_active_comment')
def filter_active_comment(comments):
    return comments.filter(is_publish=True)

