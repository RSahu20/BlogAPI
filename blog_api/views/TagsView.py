import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from blog_api.models import Tag
from blog_api.serializers.serializers import TagSerializer
from blog_api.pagination import StandardResultsSetPagination
from blog_api.permissions import WriterPermission

# Initialize logger
logger = logging.getLogger(__name__)

class TagListCreateView(APIView):
    
    """ View to list all tags and create a new tag. """
    
    permission_classes = [permissions.IsAuthenticated, WriterPermission]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        
        """
        Retrieve all tags with pagination.
        """
        try:
            tags = Tag.objects.all().order_by('id')  # Order the queryset
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(tags, request)
            serializer = TagSerializer(result_page, many=True)
            logger.info("Retrieved all tags successfully")
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving tags: {str(e)}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):

        """
        Create a new tag.
        """
        serializer = TagSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                logger.info("Created a new tag successfully")
                return Response({
                    'message': 'Tag created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            logger.warning(f"Invalid data for creating tag: {serializer.errors}")
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating tag: {str(e)}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
