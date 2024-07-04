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
        fields = ['id','title', 'content', 'publication_date', 'author']
        depth = 1
    # author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ['title', 'content', 'author']

    def validate(self, data):
        user = User.objects.get(id= data['author'].id)
        if not user:   
            raise serializers.ValidationError("Invalid user")
        return data
    
    def create(self, validated_data):
        print("inside create function")
        blog = Blogs.objects.create(title = validated_data['title'],
                                    content = validated_data['content'], author = validated_data['author'])
        blog.save()
        return validated_data