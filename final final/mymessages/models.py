from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils.text import slugify

class CustomUser (AbstractUser ):
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    full_name = models.CharField(max_length=100, blank=True)  # 姓名
    birthday = models.DateField(null=True, blank=True)  # 生日
    address = models.CharField(max_length=255, blank=True)  # 地址
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # 個人照片

class Message(models.Model):
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

def generate_unique_slug(instance):
    slug = slugify(instance.title)  # 使用標題生成初始slug
    unique_slug = slug
    counter = 1
    while Message.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"  # 添加數字以確保唯一性
        counter += 1
    return unique_slug

class Comment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)