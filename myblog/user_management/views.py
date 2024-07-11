from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . serilaizer import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class RegisterAPI(APIView):
    permission_classes = []
    def post(self, request):
        _data = request.data
        serializer = RegisterSerializer(data= _data)

        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'message': 'User created'}, status= status.HTTP_201_CREATED)

class LoginAPI(APIView):
    permission_classes = []

    def post(self, request):
        _data = request.data
        serializer = LoginSerializer(data = _data)

        if not serializer.is_valid():
            return Response({'message': 'Invalid credentials'}, status= status.HTTP_404_NOT_FOUND)
        user = authenticate(username= serializer.data['username'], password= serializer.data['password'])

        if not user:
            return Response({'message': 'Invalid user'}, status= status.HTTP_401_UNAUTHORIZED)

        token, _= Token.objects.get_or_create(user= user)

        return Response({'message': 'Login successful', 'token': str(token), 'user_id': user.id }, status= status.HTTP_201_CREATED)
    
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Succesfully Logged out'}, status=status.HTTP_200_OK)
