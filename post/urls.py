from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:pk>/like/', views.post_like_toggle, name='post_like'),
    path('<int:pk>/comment/<int:comment_pk>/like/', views.comment_like_toggle, name='comment_like'),
]