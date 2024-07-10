from django.urls import path, include
from user_management.views import RegisterAPI, LoginAPI, LogoutAPI
from blogs.views import get_blogs, create_blog, edit_blog, delete_blog, create_comment, delete_comment, get_my_blogs


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('create-blog/', create_blog, name='create_blog'), #Blog 
    path('edit-blog/', edit_blog, name='edit_blog'),       #Blog
    path('delete-blog/', delete_blog, name='delete_blog'), #Blog
    path('all-blogs/', get_blogs, name='get_blogs'),       #Blog
    path('my-blogs/', get_my_blogs, name='my_blogs'),       #Blog
    path('create-comment/', create_comment, name='create_comment'),       #comment
    path('delete-comment/', delete_comment, name='delete_comment'),       #comment
]