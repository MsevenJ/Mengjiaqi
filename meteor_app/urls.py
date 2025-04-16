from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.meteor_shower_prediction, name='meteor_shower_prediction'),
    path('astronomy-calendar/', views.astronomy_calendar, name='astronomy_calendar'),
    path('navbar/', views.navbar, name='navbar'),
    path('get-astronomy-events/', views.get_astronomy_events, name='get_astronomy_events'),
    path('import-ics-data/', views.import_ics_data, name='import_ics_data'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='index'),
    path('forum/', views.forum_index, name='forum_index'),
    path('forum/post/<int:post_id>/', views.forum_post_detail, name='forum_post_detail'),
    path('forum/post/new/', views.forum_post_new, name='forum_post_new'),
    path('forum/post/<int:post_id>/comment/', views.forum_post_comment, name='forum_post_comment'),
    path('forum/post/<int:post_id>/favorite/', views.forum_post_favorite, name='forum_post_favorite'),
    path('forum/search/', views.forum_search, name='forum_search'),

]