from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', Login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('profile_save/', profile_save, name='profile_save'),
    path('change_password/', change_password, name='change'),
    path('search/', search, name='search'),
    path('create_post/', create_view, name='create'),
    path('category/<str:title>/', categorys, name='category'),
    path('user_posts/<int:user_id>/', user_posts, name='userposts'),
    path('post_details/<int:id>', post_detail_view, name='postdate'),
    path('delete_posts/<int:pk>/', delete_post.as_view(), name='deleted'),
    path('edit_post/<int:pk>/', edit_view.as_view(), name='edit'),
    path('commentposts/<int:id>/', comments, name='comments'),
    path('reply/<int:id>/<int:comment_id>/', reply, name='reply'),
    path('like/<int:id>/', like_view, name='liked'),
    path('follow/<int:user_id>/', follwer_follwing_view, name='follow'),
    path('reset/', resetpassword.as_view(), name='reset'),
    path('reset/password/', forgetpassword.as_view(), name='forgetpassword'),
    path('confirm/<uidb64>/<token>/', confirm_password.as_view(), name='password_reset_confirm'),
    path('confirm/done/', complete.as_view(), name='complete'),
    path('follower_list/<int:user_id>', follower_list, name='follower_list'),
    path('explore/', explore, name='explore'),
]
