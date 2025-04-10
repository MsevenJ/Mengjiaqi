# meteor_app/templatetags/custom_tags.py
from django import template
import calendar
from datetime import datetime, date

register = template.Library()

@register.filter
def get_calendar(date):
    cal = calendar.monthcalendar(date.year, date.month)
    return cal

@register.filter
def make_date(date_obj):
    if isinstance(date_obj, date):
        return date_obj
    try:
        return datetime.strptime(str(date_obj), '%Y-%m-%d').date()
    except ValueError:
        return None