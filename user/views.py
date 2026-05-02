from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "아이디 또는 비밀번호가 틀렸습니다.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    
    return redirect('home')

def home_view(request):
    return render(request, 'home.html')

@login_required
def mypage(request):
    user = request.user
    posts = user.post_set.all()

    return render(request, 'mypage.html', {
        'user': user,
        'posts': posts
    })

@login_required
def check_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        user = authenticate(
            username=request.user.username,
            password=password
        )

        if user:
            request.session['verified'] = True
            return redirect('edit_profile')
        else:
            return render(request, 'check_password.html', {
                'error': '비밀번호가 틀렸습니다.'
            })

    return render(request, 'check_password.html')

@login_required
def edit_profile(request):

    if not request.session.get('verified'):
        return redirect('check_password')

    if request.method == 'POST':
        user = request.user

        user.nickname = request.POST.get('nickname')
        user.username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password:
            if new_password != confirm_password:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
                return redirect('edit_profile')

            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()

        request.session['verified'] = False
        messages.success(request, "정보 수정 완료!")
        
        return redirect('mypage')

    return render(request, 'edit_profile.html')