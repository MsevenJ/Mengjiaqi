# meteor_app/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 检查请求的路径是否为用户管理页面
        if request.path == reverse('user_management'):
            if not request.user.is_authenticated:
                # 用户未登录，重定向到登录页面
                return redirect('login')
            elif not request.user.is_admin:
                # 用户已登录但不是管理员，返回 403 错误或重定向到其他页面
                return redirect('some_other_page')  # 替换为实际的页面 URL

        response = self.get_response(request)
        return response