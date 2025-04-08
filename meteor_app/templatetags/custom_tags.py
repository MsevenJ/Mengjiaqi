# meteor_app/templatetags/custom_tags.py
from django import template
import calendar
from datetime import datetime

register = template.Library()

@register.filter
def get_calendar(date):
    cal = calendar.monthcalendar(date.year, date.month)
    return cal

@register.filter
def make_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None