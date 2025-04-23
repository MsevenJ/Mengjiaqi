# meteor_app/signals.py
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_email_verification(sender, instance, created, **kwargs):
    if created:
        subject = '邮箱验证'
        message = f'请点击以下链接验证你的邮箱：{settings.BASE_URL}/verify_email/{instance.id}/'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)