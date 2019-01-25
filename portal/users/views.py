from rest_framework import viewsets
from users.models import User, Post
from users.serializers import UserSerializer, PostSerializer
from django.contrib.auth import authenticate
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def login(self, email, password):
        """Authenticate user with given email & password"""

        user = authenticate(email=email, password=password)
        if user:
            serializer = UserSerializer(user, many=False)
            token, _ = Token.objects.get_or_create(user=user)
            user_data = serializer.data
            user_data['token'] = token.key
            return Response({
                'data': user_data,
                'status_code': HTTP_200_OK
            })

        return Response({
            'error': 'Invalid Credentials',
            'error_code': HTTP_404_NOT_FOUND
        })

    def signup(self, user_data):
        """Creates new user"""
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.get(user=user)
                user_data = serializer.data
                user_data['token'] = token.key
            return Response({
                'data': user_data,
                'status_code': HTTP_200_OK
            })
        return Response({
            'error': 'User with this email address already exists',
            'error_code': HTTP_400_BAD_REQUEST
        })

    def create(self, request, format=None):
        """
            Create new user
        """
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        cnic = request.data.get('cnic')
        if not email or not password:
            return Response({
                'error': 'Email/Password is required',
                'error_code': HTTP_400_BAD_REQUEST
            })
        if not first_name and not last_name and not cnic:
            return self.login(email, password)

        return self.signup(request.data)

    def list(self, request, format=None):
        """
            Get all users
        """

        queryset = User.objects.all()
        serializer_class = UserSerializer(queryset, many=True)
        return Response(serializer_class.data, status=HTTP_200_OK)

    def partial_update(self, request, pk, format=None):
        """
            Update User object
        """
        try:
            queryset = User.objects.get(pk=pk)
            querysettoken = request.user
            if queryset.email == querysettoken.email:
                user = UserSerializer().update(
                    instance=queryset, validated_data=request.data)
                serializer_class = UserSerializer(user, many=False)
                return Response({
                    'data': serializer_class.data,
                    'status_code': HTTP_200_OK
                })
            else:
                return Response({
                    'error': 'User does not match',
                    'error_code': HTTP_400_BAD_REQUEST
                })
        except Exception as exc:
            return Response({
                'error': str(exc),
                'error_code': HTTP_400_BAD_REQUEST
            })


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def create(self, request, format=None):
        """
            Create New Post
        """

        try:
            post_data = request.data.copy()
            post_data['user'] = request.user.id
            serializer = PostSerializer(data=post_data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    return Response({
                        'data': serializer.data,
                        'status_code': HTTP_200_OK
                    })
            return Response({
                'error': 'Invalid JSON data',
                'error_code': HTTP_400_BAD_REQUEST
            })
        except Exception as exc:
            return Response({
                'error': str(exc),
                'error_code': HTTP_400_BAD_REQUEST
            })

    def list(self, request, format=None):
        """
            Get all posts
        """
        if str(request.user):
            queryset = Post.objects.all()
            serializer_class = PostSerializer(queryset, many=True, context={'user': str(request.user)})
            return Response(serializer_class.data, status=HTTP_200_OK)
        else:
            return Response({
                'error': 'user does not exists',
                'error_code': HTTP_400_BAD_REQUEST
            })

    def partial_update(self, request, pk=None, format=None):
        """
            Update Post object
        """
        try:
            post = Post.objects.get(pk=pk, user=request.user)
            if post:
                response = super(PostView, self).partial_update(
                    request, pk, format)

                return Response({
                    'data': response.data,
                    'status_code': HTTP_200_OK
                })
        except Post.DoesNotExist:
            return Response({
                'error': 'post does not belong to the user',
                'error_code': HTTP_404_NOT_FOUND
            })
