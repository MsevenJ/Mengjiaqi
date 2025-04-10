from django.urls import path
from. import views

urlpatterns = [
    path('predict/', views.meteor_shower_prediction, name='meteor_shower_prediction'),

    # 日历
    path('astronomy-calendar/', views.astronomy_calendar, name='astronomy_calendar'),

    path('navbar/', views.navbar, name='navbar'),

    path('get-astronomy-events-by-year/', views.get_astronomy_events_by_year, name='get_astronomy_events_by_year'),

]