from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, MessageForm, UserProfileForm,CommentForm
from .models import Message,Comment
from django.http import HttpResponse
from django.utils.text import slugify


#--------
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '註冊成功！')
            return redirect('message_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'mymessages/signup.html', {'form': form})
#--------
def logout_view(request):
    logout(request)
    return redirect('message_list')
#--------
def generate_unique_slug(instance):
    slug = slugify(instance.title)  # 使用標題生成初始slug
    unique_slug = slug
    counter = 1
    while Message.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"  # 添加數字以確保唯一性
        counter += 1
    return unique_slug
#--------
# message_list 視圖
def message_list(request):
    messages_list = Message.objects.order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, '請先登入')
            return redirect('login')
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False) #commit=False 代表先不要存
            message.user = request.user
            message.slug = generate_unique_slug(message)
            message.save() #到這邊再存
            messages.success(request, '文章發布成功！')
            return redirect('message_list')
    else:
        form = MessageForm()
    
    return render(request, 'mymessages/message_list.html', {
        'messages_list': messages_list, 
        'form': form
    })
#--------
@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, '文章已更新')
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    
    return render(request, 'mymessages/edit_message.html', {
        'form': form, 
        'message': message
    })
#--------
@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)
    
    if request.method == 'POST':
        message.delete()
        messages.success(request, '文章已刪除')
        return redirect('message_list')
    
    return render(request, 'mymessages/delete_message.html', {
        'message': message
    })
#--------
@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, '個人資料已更新！')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'mymessages/userprofile.html', {'form': form})
#--------
def post_detail(request, slug):
    post = get_object_or_404(Message, slug=slug)
    return render(request, 'mymessages/post_detail.html', {'message': post})
#--------
def post_detail(request, slug):
    message = get_object_or_404(Message, slug=slug)
    comments = message.comments.all()  # 確保取出與該消息相關的所有留言

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, '請先登入才能留言')
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.message = message  # 關聯留言到這條消息
            comment.user = request.user  # 關聯留言到當前用戶
            comment.save()
            messages.success(request, '留言成功！')
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'mymessages/post_detail.html', {
        'message': message,
        'comments': comments,  # 傳遞留言到模板
        'form': form,
    })


    
def fix_slugs(request):
    messages = Message.objects.filter(slug="")
    for message in messages:
        base_slug = slugify(message.title)
        unique_slug = base_slug
        counter = 1
        while Message.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        message.slug = unique_slug
        message.save()
    return HttpResponse("Slug 補全完成")
