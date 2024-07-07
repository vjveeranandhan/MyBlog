from django.urls import path, include
from user_management.views import RegisterAPI, LoginAPI, LogoutAPI
from blogs.views import get_blogs, create_blog, edit_blog, delete_blog


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('create-blog/', create_blog, name='create_blog'),
    path('edit-blog/', edit_blog, name='edit_blog'),
    path('delete-blog/', delete_blog, name='delete_blog'),
    path('all-blogs/', get_blogs, name='get_blogs'),
]