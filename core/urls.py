from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('u/<str:username>/', views.profile_view, name='profile'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('user/<int:user_id>/follow/', views.toggle_follow, name='toggle_follow'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
