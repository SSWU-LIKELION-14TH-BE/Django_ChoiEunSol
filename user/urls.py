from django.urls import path
from .views import signup_view, login_view, logout_view, home_view, profile, edit_profile, check_password, guestbook, guestbook_create, guestbook_delete
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html'
         ),
         name='password_reset'),

    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('profile/<int:user_id>/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/password/', check_password, name='check_password'),
    path('guestbook/<int:user_id>/', guestbook, name='guestbook'),
    path('guestbook/<int:user_id>/create/', guestbook_create, name='guestbook_create'),
    path('guestbook/<int:user_id>/delete/<int:guestbook_id>/', guestbook_delete, name='guestbook_delete'),
]