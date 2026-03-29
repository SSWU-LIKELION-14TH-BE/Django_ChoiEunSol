from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import SignUpForm

def signup_view(request):
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '아이디 또는 비밀번호가 틀렸습니다.'})

    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
    return redirect('home')

def home_view(request):
    return render(request, 'home.html')

User = get_user_model()
def password_reset_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            return render(request, 'password_reset.html', {
                'error': '비밀번호가 일치하지 않습니다.'
            })
        
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('login')
        except User.DoesNotExist:
            return render(request, 'password_reset.html', {
                'error': '존재하지 않는 사용자입니다.'
            })

    return render(request, 'password_reset.html')