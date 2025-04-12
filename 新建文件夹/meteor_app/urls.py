from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.meteor_shower_prediction, name='meteor_shower_prediction'),
    path('astronomy-calendar/', views.astronomy_calendar, name='astronomy_calendar'),
    path('navbar/', views.navbar, name='navbar'),
    path('get-astronomy-events/', views.get_astronomy_events, name='get_astronomy_events'),
    path('import-ics-data/', views.import_ics_data, name='import_ics_data'),
]