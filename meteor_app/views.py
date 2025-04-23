import logging
from django.templatetags.static import static
from .moon_phase_image import get_date_image
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import ForumPost, ForumComment, ForumFavorite
from .forms import ForumPostForm
from django.http import JsonResponse
import pandas as pd
from .models import MeteorShower,CustomUser, Announcement,AstronomyEvent,Planet, AstronomyEventSubscription
from django.http import HttpResponse
import re
from datetime import datetime, date, time
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
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
            error_message = "用户名或密码错误"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("表单验证通过，用户已保存")  # 添加调试信息
            return redirect('login')  # 注册成功后重定向到登录页面
        else:
            print("表单验证失败:", form.errors)  # 添加调试信息
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def astronomy_calendar(request):
    today = datetime.today()
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


@login_required
def forum_index(request):
    posts = ForumPost.objects.all().order_by('-created_at')
    return render(request, 'forum/index.html', {'posts': posts})

@login_required
def forum_post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    comments = ForumComment.objects.filter(post=post).order_by('created_at')
    is_favorite = ForumFavorite.objects.filter(post=post, user=request.user).exists()
    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments, 'is_favorite': is_favorite})

@login_required
def forum_post_new(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('forum_post_detail', post_id=post.id)
    else:
        form = ForumPostForm()
    return render(request, 'forum/post_new.html', {'form': form})

@login_required
def forum_post_comment(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            ForumComment.objects.create(post=post, author=request.user, content=content)
    return redirect('forum_post_detail', post_id=post.id)

@login_required
def forum_post_favorite(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    favorite, created = ForumFavorite.objects.get_or_create(post=post, user=request.user)
    if not created:
        favorite.delete()
    return redirect('forum_post_detail', post_id=post.id)

@login_required
def forum_search(request):
    query = request.GET.get('q')
    if query:
        posts = ForumPost.objects.filter(title__icontains=query)
    else:
        posts = ForumPost.objects.all()
    return render(request, 'forum/index.html', {'posts': posts})

#处理流星雨数据
def parse_date(date_str, year=2025):
    if isinstance(date_str, datetime):
        date_str = date_str.strftime('%d-%b')
    cleaned_date_str = re.sub(r'[()（）]', '', date_str)
    try:
        # 尝试按 '%d-%b-%Y' 格式解析
        date_obj = datetime.strptime(f'{cleaned_date_str}-{year}', '%d-%b-%Y')
        return date_obj.date()
    except ValueError:
        try:
            # 尝试按 'YYYY-MM-DD HH:MM:SS' 格式解析
            date_obj = datetime.strptime(cleaned_date_str, '%Y-%m-%d %H:%M:%S')
            return date_obj.date()
        except ValueError as e:
            logger.debug(f"Failed to parse date '{date_str}': {e}")
            return None
#处理流星雨数据
def parse_angle(angle_str):
    cleaned = re.sub(r'[^\d.-]', '', angle_str)
    try:
        return float(cleaned)
    except ValueError as e:
        logger.debug(f"Failed to parse angle '{angle_str}': {e}")
        return None
#处理流星雨数据
def parse_maximum_lambda(value):
    try:
        cleaned_value = re.sub(r'[^\d.]', '', value)
        return float(cleaned_value)
    except (ValueError, TypeError) as e:
        logger.debug(f"Failed to parse maximum lambda '{value}': {e}")
        return None
#处理流星雨数据
def import_meteor_shower_data(request):
    try:
        # 指定 Maximum_Date 列为字符串类型
        df = pd.read_excel('meteor_shower_2025.xlsx', dtype={'Maximum_Date': str})
        for index, row in df.iterrows():
            logger.debug(f"Processing row {index}: {row}")

            name = row['Shower']
            activity = row['Activity']
            maximum_date_str = row['Maximum_Date']
            maximum_date = parse_date(maximum_date_str)
            if maximum_date is None:
                logger.warning(f"Skipping row {index} due to invalid maximum date: {maximum_date_str}")
                continue

            maximum_lambda_str = row['Maximum_λ⊙']
            maximum_lambda = parse_maximum_lambda(maximum_lambda_str)
            if maximum_lambda is None:
                logger.warning(f"Skipping row {index} due to invalid maximum lambda: {maximum_lambda_str}")
                continue

            radiant_ra_str = row['Radiant_α']
            radiant_ra = parse_angle(radiant_ra_str)
            if radiant_ra is None:
                logger.warning(f"Skipping row {index} due to invalid radiant α: {radiant_ra_str}")
                continue

            radiant_dec_str = row['Radiant_δ']
            radiant_dec = parse_angle(radiant_dec_str)
            if radiant_dec is None:
                logger.warning(f"Skipping row {index} due to invalid radiant δ: {radiant_dec_str}")
                continue

            try:
                velocity = float(row['V∞（km/s）'])
            except ValueError as e:
                logger.warning(f"Skipping row {index} due to invalid velocity: {row['V∞（km/s）']}, {e}")
                continue

            try:
                r_value = float(row['r'])
            except ValueError as e:
                logger.warning(f"Skipping row {index} due to invalid r value: {row['r']}, {e}")
                continue

            try:
                zhr = int(row['ZHR'])
            except ValueError as e:
                logger.warning(f"Skipping row {index} due to invalid ZHR: {row['ZHR']}, {e}")
                continue

            MeteorShower.objects.get_or_create(
                name=name,
                activity=activity,
                maximum_date=maximum_date,
                maximum_lambda=maximum_lambda,
                radiant_ra=radiant_ra,
                radiant_dec=radiant_dec,
                velocity=velocity,
                r_value=r_value,
                zhr=zhr
            )
            logger.debug(f"Successfully imported row {index}")

        return HttpResponse("Meteor shower data imported successfully.")
    except Exception as e:
        logger.error(f"Error importing data: {e}")
        return HttpResponse(f"Error importing data: {str(e)}")


def meteor_shower_prediction(request):
    # 获取当前的日期和时间
    now = datetime.now()
    # 使用 now 进行查询
    upcoming_showers = MeteorShower.objects.filter(maximum_date__gte=now).order_by('maximum_date')
    if upcoming_showers.exists():
        default_shower = upcoming_showers.first()
    else:
        default_shower = None
    return render(request, 'meteor_shower_prediction.html',
                  {'upcoming_showers': upcoming_showers, 'default_shower': default_shower})


@login_required
def my_profile(request):
    astronomy_events = AstronomyEvent.objects.all()  # 这里先简单获取所有天象活动，后续可根据实际需求过滤
    return render(request, 'my_profile.html', {
        'astronomy_events': astronomy_events,
        'selected_function': None
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        # 这里可以添加更新个人信息的逻辑
        return redirect('my_profile')
    return render(request, 'my_profile.html', {'selected_function': 'update_profile'})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            logout(request)
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'my_profile.html', {'selected_function': 'change_password'})

@login_required
def view_favorite_posts(request):
    favorite_posts = ForumFavorite.objects.filter(user_id=request.user.id)
    return render(request, 'my_profile.html', {
        'favorite_posts': favorite_posts,
        'selected_function': 'view_favorite_posts'
    })

@login_required
def view_my_posts(request):
    my_posts = ForumPost.objects.filter(author=request.user)
    return render(request, 'my_profile.html', {
        'my_posts': my_posts,
        'selected_function': 'view_my_posts'
    })

@login_required
def view_astronomy_events(request):
    return render(request, 'my_profile.html', {'selected_function': 'view_astronomy_events'})

@login_required
def view_reminders(request):
    return render(request, 'my_profile.html', {'selected_function': 'view_reminders'})

def solar_system_view(request):
    return render(request, '3D-CSS-Solar-System-master/index.html')

def search_bar(request):
    return render(request, 'search_bar.html')


def is_admin(user):
    return user.is_admin

@user_passes_test(is_admin)
def user_management(request):
    users = CustomUser.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = CustomUser.objects.get(id=user_id)
        if action == 'ban':
            user.is_banned = True
            user.save()
        elif action == 'unban':
            user.is_banned = False
            user.save()
    return render(request, 'user_management.html', {'users': users})

@user_passes_test(is_admin)
def publish_announcement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        Announcement.objects.create(title=title, content=content, author=author)
        return redirect('announcement_list')
    return render(request, 'publish_announcement.html')

@user_passes_test(is_admin)
def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'announcement_list.html', {'announcements': announcements})

def read_announcements(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'read_announcements.html', {'announcements': announcements})

@csrf_exempt
@login_required
def subscribe_to_event(request, event_id):
    try:
        logger.info(f'收到订阅请求，事件 ID: {event_id}')
        event = AstronomyEvent.objects.get(id=event_id)
        subscription, created = AstronomyEventSubscription.objects.get_or_create(
            user=request.user,
            event=event
        )
        if created:
            logger.info(f'用户 {request.user.username} 成功订阅事件 {event_id}')
            return JsonResponse({'status': 'success', 'message': '订阅成功', 'subscribed': True})
        else:
            subscription.subscribed = not subscription.subscribed
            subscription.save()
            logger.info(f'用户 {request.user.username} 更改订阅状态为 {subscription.subscribed} 事件 {event_id}')
            return JsonResponse({'status': 'success', 'message': '订阅状态已更新', 'subscribed': subscription.subscribed})
    except AstronomyEvent.DoesNotExist:
        logger.error(f'事件 ID {event_id} 不存在')
        return JsonResponse({'status': 'error', 'message': '事件不存在', 'subscribed': False})
    except Exception as e:
        logger.error(f'订阅过程中出现错误: {str(e)}')
        return JsonResponse({'status': 'error', 'message': '订阅过程中出现错误，请稍后重试', 'subscribed': False})