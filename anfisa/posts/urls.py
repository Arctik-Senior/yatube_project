from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('group/', views.group_list, name='group_lists'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='create_post'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('group/<slug:slug>/', views.group_list, name="group_list"),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),  # noqa: E501
    path('follow/', views.follow_index, name='follow_index'),    
    path(
        'profile/<str:username>/follow/',
        views.profile_follow, 
        name='profile_follow'
    ),

    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),

    path('', views.index, name='index'),
]
