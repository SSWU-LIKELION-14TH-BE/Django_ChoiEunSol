from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Guestbook

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
def check_password(request):
    # 소셜 로그인 유저인지 확인
    if request.user.socialaccount_set.exists():
        request.session['verified'] = True
        return redirect('edit_profile')
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

        if CustomUser.objects.exclude(pk=user.pk).filter(username=request.POST.get('username')).exists():
            messages.error(request, "이미 존재하는 아이디입니다.")
            return redirect('edit_profile')

        user.save()

        request.session['verified'] = False
        messages.success(request, "정보 수정 완료!")

        return redirect('profile', user_id=request.user.id)

    return render(request, 'edit_profile.html')

def profile(request, user_id):
    user_obj = get_object_or_404(CustomUser, pk=user_id)

    posts = user_obj.post_set.all()
    guestbooks = user_obj.guestbooks.all().order_by('-created_at')

    return render(request, 'profile.html', {
        'profile_user': user_obj,
        'posts': posts,
        'guestbooks': guestbooks
    })

def guestbook(request, user_id):
    owner = get_object_or_404(CustomUser, pk=user_id)
    guestbook_list = owner.guestbooks.all()

    return render(request, 'guestbook.html', {
        'owner': owner,
        'guestbook_list': guestbook_list
    })

@login_required
def guestbook_create(request, user_id):
    owner = get_object_or_404(CustomUser, pk=user_id)

    if owner == request.user:
        return redirect('guestbook', user_id=user_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Guestbook.objects.create(
                owner=owner,
                author=request.user,
                content=content
            )

    return redirect('guestbook', user_id=user_id)

@login_required
def guestbook_delete(request, user_id, guestbook_id):
    guestbook = get_object_or_404(Guestbook, pk=guestbook_id)

    if guestbook.author != request.user:
        return redirect('guestbook', user_id=user_id)

    if request.method == 'POST':
        guestbook.delete()

    return redirect('guestbook', user_id=user_id)