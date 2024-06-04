from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.register, name='signup'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('profile/', views.edit_profile, name='profile'),
    # path('home/', views.home, name='home'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('explore/', views.explore, name='explore'),
    path('groups/', views.groups, name='groups'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('phome/', views.phome, name='phome'),
    path('admin/delete_posts/', views.delete_all_posts, name='delete_all_posts'),
]
