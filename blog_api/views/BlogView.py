import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from blog_api.models import Post
from blog_api.serializers.PostSerializer import PostSerializer
from blog_api.pagination import StandardResultsSetPagination
from blog_api.permissions import WriterPermission, ReadOnlyPermission

logger = logging.getLogger(__name__)

class BlogListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, WriterPermission | ReadOnlyPermission]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        """
        Retrieve all blog posts with pagination.
        """
        try:
            posts = Post.objects.all().order_by('id')  # Order the queryset
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(result_page, many=True)
            logger.info("Retrieved all blog posts successfully")
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving blog posts: {str(e)}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new blog post.
        """
        serializer = PostSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                logger.info("Created a new blog post successfully")
                return Response({'message': 'Blog entry created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            logger.warning(f"Invalid data for creating blog post: {serializer.errors}")
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating blog post: {str(e)}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleBlogView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, WriterPermission | ReadOnlyPermission]

    def get_object(self, id):
        """
        Retrieve a blog post by its ID.
        """
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None

    def get(self, request, id):
        """
        Retrieve a single blog post.
        """
        try:
            post = self.get_object(id)
            if not post:
                logger.warning(f"Post with id {id} not found")
                return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(post)
            logger.info(f"Retrieved post with id {id} successfully")
            return Response({'message': 'Retrieve post successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving post with id {id}: {str(e)}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        """
        Update a single blog post.
        """
        try:
            post = self.get_object(id)
            if not post:
                logger.warning(f"Post with id {id} not found")
                return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated post with id {id} successfully")
                return Response({'message': 'Post updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            logger.warning(f"Invalid data for updating post with id {id}: {serializer.errors}")
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating post with id {id}: {str(e)}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        """
        Delete a single blog post.
        """
        try:
            post = self.get_object(id)
            if not post:
                logger.warning(f"Post with id {id} not found")
                return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            post.delete()
            logger.info(f"Deleted post with id {id} successfully")
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting post with id {id}: {str(e)}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
