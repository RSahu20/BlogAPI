from django.contrib.auth.models import User
from rest_framework import status
from django.core.exceptions import ValidationError
from accounts.password_validator import CustomPasswordValidator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import IntegrityError
from .models import UserProfile
from django.contrib.auth import authenticate

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            role = request.data.get('role').lower()  # Normalize to lowercase
            bio = request.data.get('bio', '')  # Optional bio field

            # Validate the role
            if role not in ['writer', 'commenter']:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid role. Allowed roles are "writer" and "commenter".'
                })

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Username already exists'
                })
            
            password_validator = CustomPasswordValidator()
            try:
                password_validator.validate(password)
            except ValidationError as e:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Password validation failed',
                    'details': e.messages
                })
            
            # Create a new user
            user = User.objects.create_user(username=username, password=password)

            # Create a UserProfile instance with the selected role and optional bio
            UserProfile.objects.create(user=user, role=role, bio=bio)

            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'User created successfully'
            })

        except IntegrityError as e:
            # Handle database integrity errors
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Database integrity error',
                'details': str(e)
            })
        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An unexpected error occurred',
                'details': str(e)
            })

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                token = get_tokens(user)
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'Login successful',
                    'token': token
                })

            return Response({
                'status': status.HTTP_401_UNAUTHORIZED,
                'message': 'Invalid credentials'
            })

        except IntegrityError as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Database integrity error',
                'details': str(e)
            })
        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An unexpected error occurred',
                'details': str(e)
            })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'An error occurred during logout',
                'details': str(e)
            })


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')

            # Debugging output
            print(old_password)
            print(new_password)
            if not old_password or not new_password:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Old password and new password must be provided.'
                })

            # Check if the old password is correct
            if not user.check_password(old_password):
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Old password is incorrect'
                })

            # Validate the new password
            password_validator = CustomPasswordValidator()
            try:
                password_validator.validate(new_password, user=user)
            except ValidationError as e:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Password validation failed',
                    'details': e.messages
                })

            # Set the new password and save
            user.set_password(new_password)
            user.save()  # The signal will automatically handle saving the new password to history

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Password changed successfully'
            })

        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An unexpected error occurred',
                'details': str(e)
            })