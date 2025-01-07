from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Message,Comment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nickname']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content']
        widgets = {
            'title': forms.Textarea(attrs={
                'rows': 1, 
                'placeholder': '請輸入標題', 
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': '請輸入內文', 
                'class': 'form-control'
            })
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser 
        fields = ['full_name', 'birthday', 'email', 'address', 'profile_picture']
        
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
