from django.core.mail import send_mail
from django.utils import timezone
from .models import AstronomyEvent, AstronomyEventSubscription

def send_event_reminders():
    tomorrow = timezone.now().date() + timezone.timedelta(days=1)
    events = AstronomyEvent.objects.filter(start_date=tomorrow)
    for event in events:
        subscriptions = AstronomyEventSubscription.objects.filter(event=event, subscribed=True)
        for subscription in subscriptions:
            user = subscription.user
            subject = f'天文事件提醒：{event.summary}'
            message = f'尊敬的用户，天象 {event.summary} 将在明天（{tomorrow}）开始，详情：{event.description}'
            send_mail(
                subject,
                message,
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )