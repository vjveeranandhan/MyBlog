from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blogs   

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Blogs
        fields = ['id', 'title', 'content', 'publication_date', 'author']
        depth = 1
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())