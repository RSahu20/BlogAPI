from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Tag, Category, Post, Comment
from .serializer.serializers import PostSerializer, CommentSerializer, CategorySerializer, TagSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Retrieve all categories successfully',
            'data': serializer.data
        })

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Category created successfully',
                'data': serializer.data
            })
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors
        })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def blog_post_view(request):
    pagination_class = StandardResultsSetPagination

    try:
        if request.method == 'GET':
            posts = Post.objects.all().order_by('id')
            paginator = pagination_class()
            result_page = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        elif request.method == 'POST':
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': status.HTTP_201_CREATED,
                    'message': 'Blog entry created successfully',
                    'data': serializer.data
                })
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors
            })
    except IntegrityError as e:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })
    except Exception as e:
        return Response({
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': str(e)
        })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tag_view(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Retrieve all tags successfully',
            'data': serializer.data
        })

    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Tag created successfully',
                'data': serializer.data
            })
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors
        })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_view(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Retrieve all comments successfully',
            'data': serializer.data
        })

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Comment added successfully',
                'data': serializer.data
            })
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors
        })


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_post_view(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'Post not found'
        })

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Retrieve post successfully',
            'data': serializer.data
        })

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Post updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors
        })

    elif request.method == 'DELETE':
        post.delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Post deleted successfully'
        })


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_comment_view(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'Comment not found'
        })

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Retrieve comment successfully',
            'data': serializer.data
        })

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Comment updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors
        })

    elif request.method == 'DELETE':
        comment.delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Comment deleted successfully'
        })


@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'status': status.HTTP_201_CREATED,
            'message': 'User registered successfully',
            'data': {
                'token': token.key
            }
        })
    return Response({
        'status': status.HTTP_400_BAD_REQUEST,
        'message': serializer.errors
    })


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Login successful',
                'data': {
                    'token': token.key
                }
            })
        else:
            return Response({
                'status': status.HTTP_401_UNAUTHORIZED,
                'message': 'Invalid credentials'
            })
    except User.DoesNotExist:
        return Response({
            'status': status.HTTP_401_UNAUTHORIZED,
            'message': 'Invalid credentials'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Attempt to delete the user's token
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Logout successful'
        })
    except Token.DoesNotExist:
        # Token not found
        raise NotFound(detail="Token not found for the user.")
    except Exception as e:
        # Any other exception
        return Response({
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': str(e)
        })