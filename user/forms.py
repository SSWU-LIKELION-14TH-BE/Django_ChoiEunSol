from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="아이디")
    email = forms.EmailField(label="이메일", required=True)
    phone_number = forms.CharField(label="전화번호")
    nickname = forms.CharField(label="닉네임")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'nickname', 'password1', 'password2']