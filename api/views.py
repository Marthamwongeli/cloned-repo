import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import logout





# Set up logging
logger = logging.getLogger(__name__)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        """
        Create a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User created successfully.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error('User creation failed: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        """
        Retrieve a list of all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info("Retrieved user list.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        queryset = User.objects.all()
        sub_location = self.request.query_params.get('first_name',None)
        if sub_location:
            queryset= queryset.filter(first_name=first_name)
        return queryset

class UserDetailView(APIView):
    """
    Handle User detail retrieval, update, and deletion.
    """
    def get(self, request, id):
        
        """
        Retrieve a user by ID.
        """
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            logger.error('User with ID %d not found.', id)
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        logger.info('User with ID %d retrieved successfully.', id)
        return Response(serializer.data)
    
    def patch(self, request, id):
        """
        Update a user by ID.
        """
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            logger.error('User with ID %d not found for update.', id)
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info('User with ID %d updated successfully.', id)
            return Response(serializer.data)
        else:
            logger.error('User update failed for ID %d: %s', id, serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RegisterView(APIView):
    # Method to handle POST requests for user registration
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class YourProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # Your view logic here
        return Response({"message": "You have access to this view!"})


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': 'Successfully logged in.',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class CreateAdminUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        first_name = request.data.get('firstname')
        last_name = request.data.get('lastname')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            return Response({"detail": "Superuser created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Superuser already exists"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def generate_token(request):
    user,created =User.objects.get_or_create(username='dummyuser')
    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        'access':str(refresh.access_token),
        'refresh':str(refresh)
    })
    


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the token to prevent reuse
            return Response({'success': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Create a token but do not include it in the response
        token = super().get_token(user)
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Call the super method to get the default response
        response = super().post(request, *args, **kwargs)
        
        # Customize the response to only include the success message
        if response.status_code == status.HTTP_200_OK:
            return Response({"message": "Successfully logged in"}, status=status.HTTP_200_OK)
        
        return response
    
    
roles = ["Admin", "Nurse", "CHP"]

class UserRoleListCreateView(APIView):
    
    # GET request to retrieve the list of roles
    def get(self, request):
        return Response({"roles": roles}, status=status.HTTP_200_OK)

    # POST request to add a new role
    def post(self, request):
        new_role = request.data.get('role')
        if new_role:
            if new_role not in roles:
                roles.append(new_role)
                return Response({"message": f"Role '{new_role}' added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Role already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "No role provided"}, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Assuming you have a User model and a UserSerializer to handle user data
        user = request.user  # Get the logged-in user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user  # Get the logged-in user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
        
