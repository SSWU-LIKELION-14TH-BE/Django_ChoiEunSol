from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="아이디")
    email = forms.EmailField(label="이메일", required=True)
    phone_number = forms.CharField(label="전화번호")
    nickname = forms.CharField(label="닉네임")

    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'nickname', 'password1', 'password2']