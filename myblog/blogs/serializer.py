from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blogs, Comments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comments
        fields = ['id', 'blog_id', 'text', 'created_at', 'author']
        depth = 1
    # author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    blog_id = serializers.PrimaryKeyRelatedField(queryset=Blogs.objects.all())

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Blogs
        fields = ['id', 'title', 'content', 'publication_date', 'author']
        depth = 1
    # author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def __str__(self):
        return self.title
    
