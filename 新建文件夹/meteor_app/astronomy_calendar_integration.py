from icalendar import Calendar, Event, Timezone
from datetime import date, datetime, timedelta
from lxml import html
import requests
import calendar
import pytz
import re
from .models import AstronomyEvent


def initCalendar():
    calendar = Calendar()
    calendar.add('version', '2.0')
    calendar.add('prodid', '-//Celestial events//seasky.org//')
    calendar.add('x-wr-calname', 'Celestial events')
    return calendar


def parseCalendar(calendar, year):
    url = 'http://www.seasky.org/astronomy/astronomy-calendar-%s.html'
    page = requests.get(url % year)
    dom = html.fromstring(page.text)
    events = dom.xpath('//div[@id="right-column-content"]/ul/li/p')
    print('Processing the year %i which contains %i events.' % (year, len(events)))
    for event in events:
        date_list = getDate(event, year)
        summary = getSummary(event)
        description = getDescription(event)
        calendar = addEvent(calendar, summary, description, date_list)
    return calendar


def getDate(event, year):
    raw = ''.join(event.xpath('span[@class="date-text"]/text()'))
    month = list(calendar.month_name).index(''.join(re.findall('[a-zA-Z]+', raw)))
    days = [int(day) for day in re.findall(r'\d+', raw)]
    return [date(year, month, days[0]), getNextDay(date(year, month, days[-1]))]


def getNextDay(date):
    return date + timedelta(days=1)


def getSummary(event):
    return ''.join(event.xpath('span[@class="title-text"]/text()')).rstrip(' .')


def getDescription(event):
    return ''.join(event.xpath('text()')).strip(' -')


def getUid(date_list, summary):
    timestamp = ''.join(map(lambda x: x.strftime('%Y%m%d'), date_list))
    summary = ''.join(summary.lower().split(' '))
    domain = 'seasky.org'
    return summary + '_' + timestamp + '@' + domain


def addEvent(calendar, summary, description, date_list):
    event = Event()
    event.add('summary', summary)
    event.add('description', description)
    event.add('dtstart', date_list[0])
    event.add('dtend', date_list[1])
    event.add('dtstamp', datetime.now())
    event['uid'] = getUid(date_list, summary)
    calendar.add_component(event)
    return calendar


def generateAstronomyCalendar():
    cal = initCalendar()
    for year in range(2015, 2031):
        cal = parseCalendar(cal, year)
    return cal



def import_ics_to_db():
    cal = generateAstronomyCalendar()
    for component in cal.walk():
        if component.name == 'VEVENT':
            event_start = component.get('dtstart').dt
            event_end = component.get('dtend').dt
            if isinstance(event_start, date) and isinstance(event_end, date):
                summary = component.get('summary')
                description = component.get('description')
                AstronomyEvent.objects.get_or_create(
                    summary=summary,
                    description=description,
                    start_date=event_start,
                    end_date=event_end
                )


