import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from blog_api.models import Comment
from blog_api.serializers.CommentSerializer import CommentSerializer
from blog_api.pagination import StandardResultsSetPagination
from blog_api.permissions import CommentPermission

logger = logging.getLogger(__name__)


class CommentListCreateView(APIView):
    
    """ View to list all comments and create a new comment. """
    
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated, CommentPermission]

    def get(self, request):
        """
        Retrieve all comments with pagination.
        """
        try:
            comments = Comment.objects.all().order_by('id')  # Order the queryset
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(comments, request)
            serializer = CommentSerializer(result_page, many=True)
            
            logger.info("Retrieved all comments successfully")
            return paginator.get_paginated_response(serializer.data)
        
        except Exception as e:
            logger.error(f"Error retrieving comments: {str(e)}")
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        """
        Create a new comment.
        """
        serializer = CommentSerializer(data=request.data)
        
        try:
            if serializer.is_valid():
                serializer.save()
                logger.info("Created a new comment successfully")
                return Response({
                    'message': 'Comment added successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            logger.warning(f"Invalid data for creating comment: {serializer.errors}")
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error creating comment: {str(e)}")
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class SingleCommentView(APIView):
    
    """ View to retrieve, update, or delete a single comment. """
    
    
    permission_classes = [permissions.IsAuthenticated, CommentPermission]


    def get_object(self, id):
        """
        Retrieve a comment by its ID.
        """
        try:
            return Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return None


    def get(self, request, id):
        """
        Retrieve a single comment.
        """
        try:
            comment = self.get_object(id)
            if not comment:
                logger.warning(f"Comment with id {id} not found")
                return Response({
                    'message': 'Comment not found'
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = CommentSerializer(comment)
            logger.info(f"Retrieved comment with id {id} successfully")
            return Response({
                'message': 'Retrieve comment successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            
            logger.error(f"Error retrieving comment with id {id}: {str(e)}")
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, id):
        """
        Update a single comment.
        """
        try:
            comment = self.get_object(id)
            if not comment:
                logger.warning(f"Comment with id {id} not found")
                return Response({
                    'message': 'Comment not found'
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated comment with id {id} successfully")
                return Response({
                    'message': 'Comment updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            logger.warning(f"Invalid data for updating comment with id {id}: {serializer.errors}")
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            
            logger.error(f"Error updating comment with id {id}: {str(e)}")
            return Response({
                'message': str(e)}
            , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, id):
        """
        Delete a single comment.
        """
        try:
            comment = self.get_object(id)
            if not comment:
                logger.warning(f"Comment with id {id} not found")
                return Response({
                    'message': 'Comment not found'
                }, status=status.HTTP_404_NOT_FOUND)
            comment.delete()
            logger.info(f"Deleted comment with id {id} successfully")
            return Response({
                'message': 'Comment deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            
            logger.error(f"Error deleting comment with id {id}: {str(e)}")
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
