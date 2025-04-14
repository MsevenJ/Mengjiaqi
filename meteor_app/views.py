import logging
from django.http import JsonResponse, HttpResponse
from django.templatetags.static import static  # 导入 static 函数
from .models import AstronomyEvent
import datetime
from .moon_phase_image import get_date_image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 检查 next 参数，如果有则重定向到该页面，否则重定向到天文日历页面
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('astronomy_calendar')
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 注册成功后重定向到登录页面
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

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
    today = datetime.date.today()
    image_path = get_date_image(today)
    if image_path is None:
        logger.warning("Failed to get moon phase image. Using default background.")
        image_path = static('default_background.jpg')  # 使用静态文件 URL
    return render(request, 'astronomy_calendar.html', {'moon_phase_image': image_path})

def navbar(request):
    return render(request, 'navbar.html')

def get_astronomy_events(request):
    date_start_str = request.GET.get('date_start')
    date_end_str = request.GET.get('date_end')
    summary = request.GET.get('summary')

    query = AstronomyEvent.objects.all()

    if date_start_str and date_end_str:
        query = query.filter(start_date__lte=date_end_str, end_date__gte=date_start_str)
    if summary:
        query = query.filter(summary__icontains=summary)

    event_list = []
    for event in query:
        event_dict = {
            'summary': str(event.summary),
            'description': str(event.description),
            'dtstart': event.start_date.strftime('%Y-%m-%d'),
            'dtend': event.end_date.strftime('%Y-%m-%d')
        }
        event_list.append(event_dict)

    logger.info(f"Fetched {len(event_list)} events for the query.")
    print(f"Fetched {len(event_list)} events for the query.")
    return JsonResponse({'events': event_list})

def import_ics_data(request):
    from .astronomy_calendar_integration import import_ics_to_db
    import_ics_to_db()
    return HttpResponse("ICS data imported successfully.")


