import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import AstronomyEvent
from datetime import date

logger = logging.getLogger(__name__)

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
    return render(request, 'astronomy_calendar.html')

def navbar(request):
    return render(request, 'navbar.html')

def get_astronomy_events(request):
    date_start_str = request.GET.get('date_start')
    date_end_str = request.GET.get('date_end')
    if date_start_str and date_end_str:
        try:
            events = AstronomyEvent.objects.filter(start_date__lte=date_end_str, end_date__gte=date_start_str)
            event_list = []
            for event in events:
                event_dict = {
                    'summary': str(event.summary),
                    'description': str(event.description),
                    'dtstart': event.start_date.strftime('%Y-%m-%d'),
                    'dtend': event.end_date.strftime('%Y-%m-%d')
                }
                event_list.append(event_dict)
            logger.info(f"Fetched {len(event_list)} events for date range {date_start_str} - {date_end_str}")
            return JsonResponse({'events': event_list})
        except Exception as e:
            logger.error(f"Error fetching events: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    logger.error("No date range provided")
    return JsonResponse({'error': 'No date range provided'}, status=400)

def import_ics_data(request):
    from .astronomy_calendar_integration import import_ics_to_db
    import_ics_to_db()
    return HttpResponse("ICS data imported successfully.")