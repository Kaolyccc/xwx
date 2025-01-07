from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from mymessages import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.message_list, name='message_list'),

    # 用戶認證/管理
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='mymessages/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),  # 修改這裡
    path('profile/', views.user_profile, name='user_profile'),

    # 留言管理
    path('message/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),

    # 文章
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]

# 添加靜態文件的路由（如果DEBUG為True）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
