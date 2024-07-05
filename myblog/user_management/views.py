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
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

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

        return Response({'message': 'Login successful', 'token': str(token)}, status= status.HTTP_201_CREATED)
    
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Succesfully Logged out'}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def index(request):
     if request.method == 'GET':
        student = {
            "student_id": 123456,
            "first_name": "John",
            "last_name": "Doe",
            "age": 20,
            "email": "john.doe@example.com",
            "courses": ["Mathematics", "Physics", "Computer Science"],
            "grades": {
                "Mathematics": "A",
                "Physics": "B+",
                "Computer Science": "A-"
            },
            "address": {
                "street": "123 Main Street",
                "city": "Anytown",
                "state": "CA",
                "zipcode": "12345"
            }}
     if request.method == 'POST':
         student = {
            "student_id": 987654,
            "first_name": "Jane",
            "last_name": "Smith",
            "age": 22,
            "email": "jane.smith@example.com",
            "courses": ["History", "Literature", "Art"],
            "grades": {
                "History": "B",
                "Literature": "A-",
                "Art": "B+"
            },
            "address": {
                "street": "456 Oak Avenue",
                "city": "Sometown",
                "state": "NY",
                "zipcode": "54321"
            }
            }

     return Response(student)