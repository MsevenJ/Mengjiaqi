from django.urls import path
from . import views

urlpatterns = [
    path('meteor-shower-prediction/', views.meteor_shower_prediction, name='meteor_shower_prediction'),
    path('solar_system/', views.solar_system_view, name='solar_system'),
    path('astronomy-calendar/', views.astronomy_calendar, name='astronomy_calendar'),
    path('subscribe-to-event/<int:event_id>/', views.subscribe_to_event, name='subscribe_to_event'),
    path('search-bar/', views.search_bar, name='search_bar'),
    path('navbar/', views.navbar, name='navbar'),
    path('get-astronomy-events/', views.get_astronomy_events, name='get_astronomy_events'),
    path('import-ics-data/', views.import_ics_data, name='import_ics_data'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='index'),


    #论坛
    path('forum/', views.forum_index, name='forum_index'),
    path('forum/post/<int:post_id>/', views.forum_post_detail, name='forum_post_detail'),
    path('forum/post/new/', views.forum_post_new, name='forum_post_new'),
    path('forum/post/<int:post_id>/comment/', views.forum_post_comment, name='forum_post_comment'),
    path('forum/post/<int:post_id>/favorite/', views.forum_post_favorite, name='forum_post_favorite'),
    path('forum/search/', views.forum_search, name='forum_search'),


    #处理流星雨数据
    path('import-meteor-shower-data/', views.import_meteor_shower_data, name='import_meteor_shower_data'),


    #“我的”界面
    path('my-profile/', views.my_profile, name='my_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('view-favorite-posts/', views.view_favorite_posts, name='view_favorite_posts'),
    path('view-my-posts/', views.view_my_posts, name='view_my_posts'),
    path('view-astronomy-events/', views.view_astronomy_events, name='view_astronomy_events'),
    path('view-reminders/', views.view_reminders, name='view_reminders'),


    #管理员、公告
    path('user_management/', views.user_management, name='user_management'),
    path('publish_announcement/', views.publish_announcement, name='publish_announcement'),
    path('announcement_list/', views.announcement_list, name='announcement_list'),
    path('read_announcements/', views.read_announcements, name='read_announcements'),
]