from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializer import BlogSerializer, BlogPostSerializer
from rest_framework import status
from . models import Blogs
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class BlogsAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        blogs = Blogs.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        print("Inside post function")
        _data = request.data
        print(_data)
        serializer = BlogPostSerializer(data= _data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_blogs(request):
    if request.method == 'GET':
        data = request.data
        print
        if data and data['id']:
            all_blogs_obj = Blogs.objects.get(id= data['id'])
            serialized_blogs = BlogSerializer(all_blogs_obj, many=False)
        else:
            all_blogs_obj = Blogs.objects.all()
            serialized_blogs = BlogSerializer(all_blogs_obj, many=True)
        return Response(serialized_blogs.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_blog(request):
    print("inside create blog")
    if request.method == 'POST':
        data = request.data
        serializer = BlogSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['PUT', 'PATCH'])
def edit_blog(request):
    if request.method == 'PUT':
        data = request.data
        blog_object = Blogs.objects.get(id=data['id'])
        serializer = BlogSerializer(blog_object, data= data, partial= False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        blog_object = Blogs.objects.get(id=data['id'])
        serializer = BlogSerializer(blog_object, data= data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
@api_view(['DELETE'])
def delete_blog(request):
    if request.method == 'DELETE':
        data = request.data
        if data['id']:
            blog_obj = Blogs.objects.get(id= data['id'])
            blog_obj.delete()
        return Response({'message':'Person deleted'})
