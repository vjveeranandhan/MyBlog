from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializer import BlogSerializer, CommentSerializer, GetBlogSerializer, GetCommentSerializer
from rest_framework import status
from . models import Blogs, Comments
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django_ratelimit.decorators import ratelimit
# Create your views here.

# Blog CRED Operations
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='10/m', block=True)
def create_blog(request):
    try:
        if request.method == 'POST':
            data = request.data
            print("data", data)
            serializer = BlogSerializer(data= data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        else:
            return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='10/m', block=True)
def get_blogs(request):
    try:
        if request.method == 'GET':
            data = request.data
            id = request.query_params.get('id')
            print(id)
            if id:
                all_blogs_obj = Blogs.objects.filter(id= id).first()
                if all_blogs_obj:
                    comment_obj = Comments.objects.filter(blog_id = all_blogs_obj.id).all()
                    serialized_comment =  CommentSerializer(comment_obj, many= True)
                    serialized_blogs = GetBlogSerializer(all_blogs_obj, many=False)
                    return Response({'blog':serialized_blogs.data, 'comments':serialized_comment.data}, status=status.HTTP_200_OK)    
                else:
                    return Response(status= status.HTTP_400_BAD_REQUEST)
            else:
                all_blogs_obj = Blogs.objects.all()
                serialized_blogs = GetBlogSerializer(all_blogs_obj, many=True, context={'request_type': 'GET'})
            return Response(serialized_blogs.data, status=status.HTTP_200_OK)    
        else:
            return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
            return Response(status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='10/m', block=True)
def get_my_blogs(request):
    try:
        if request.method == 'GET':
            author_id = request.query_params.get('author_id')
            if author_id:
                all_blogs_obj = Blogs.objects.filter(author= author_id).all()
                serialized_blogs = BlogSerializer(all_blogs_obj, many=True)
                return Response(serialized_blogs.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'author id is missing'}, status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='10/m', block=True)
def edit_blog(request):
    try:
        _data = request.data
        if request.method == 'PUT':
            if 'id' in _data and 'author' in _data:
                blog_object = Blogs.objects.filter(id=_data['id'], author = _data['author']).first()
                if blog_object:
                    serializer = BlogSerializer(blog_object, data=_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors)
                return Response([], status=status.HTTP_200_OK)
            else:
                return Response({'message': 'id is missing'}, status= status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PATCH':
            if 'id' in _data:
                blog_object = Blogs.objects.filter(id=_data['id']).first()
                serializer = BlogSerializer(blog_object, data= _data, partial= True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors)
            else:
                return Response({'message': 'id is missing'}, status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'invaid method'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='10/m', block=True)
def delete_blog(request):
    try:
        if request.method == 'DELETE':
            _data = request.data
            if 'id' in _data:
                blog_obj = Blogs.objects.filter(id= _data['id']).first()
                if blog_obj:
                    blog_obj.delete()
                    return Response({'message':'Blog deleted', 'id': _data['id']}, status=status.HTTP_200_OK)
                else:
                    return Response({'message':'blog not found'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message':'Id is missing'},  status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'invaid method'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
# Comment CRED Operations
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='10/m', block=True)
def create_comment(request):
    try:
        if request.method == 'POST':
            _data = request.data
            serializer = GetCommentSerializer(data= _data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED)
            return Response(serializer.errors)
        else:
            return Response({'message':'invaid method'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='10/m', block=True)
def delete_comment(request):
    try:
        if request.method == 'DELETE':
            _data = request.data
            if 'id' in _data and 'requested_user_id' in _data and 'blog_id' in _data:
                comment_obj =  Comments.objects.filter(id= _data['id'], author= _data['requested_user_id'],
                                                    blog_id= _data['blog_id']).first()
                if comment_obj:
                    comment_obj.delete()
                    return Response({'message':'Comment deleted', 'id': _data['id']}, status= status.HTTP_200_OK)
                return Response({'message':'comment not found'}, status= status.HTTP_400_BAD_REQUEST)
            return Response({'message':'comment id, blog id or request user is missing'}, status= status.HTTP_400_BAD_REQUEST)
        return Response({'message':'invaid method'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)