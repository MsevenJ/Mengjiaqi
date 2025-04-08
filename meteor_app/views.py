from django.shortcuts import render
from .astronomy_calendar_integration import generateAstronomyCalendar
from.models import City, Constellation, MeteorShower, MoonPhase
from datetime import date

def meteor_shower_prediction(request):
    if request.method == 'POST':
        city_name = request.POST.get('city')
        try:
            city = City.objects.get(name=city_name)
            visible_constellations = Constellation.objects.filter(
                min_latitude__lte=city.latitude,
                max_latitude__gte=city.latitude
            )
            meteor_showers = MeteorShower.objects.filter(radiant_constellation__in=visible_constellations)
            return render(request, 'prediction_result.html', {'meteor_showers': meteor_showers})
        except City.DoesNotExist:
            error_message = "City not found."
            return render(request, 'prediction_form.html', {'error_message': error_message})
    return render(request, 'prediction_form.html')

def astronomy_calendar(request):
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = date.fromisoformat(selected_date_str)
            cal = generateAstronomyCalendar()
            events = []
            for component in cal.walk():
                if component.name == 'VEVENT':
                    event_start = component.get('dtstart').dt
                    event_end = component.get('dtend').dt
                    if isinstance(event_start, date) and isinstance(event_end, date):
                        if event_start <= selected_date <= event_end:
                            event = {
                                'summary': component.get('summary'),
                                'description': component.get('description'),
                                'dtstart': event_start,
                                'dtend': event_end
                            }
                            events.append(event)
            return render(request, 'astronomy_calendar.html', {'events': events, 'selected_date': selected_date})
        except ValueError:
            pass
    return render(request, 'astronomy_calendar.html', {'events': [], 'selected_date': None})

def navbar(request):
    return render(request, 'navbar.html')