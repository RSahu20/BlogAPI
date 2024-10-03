# from blog_api.pagination import StandardResultsSetPagination
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.db import IntegrityError
# from blog_api.models import Tag, Category, Post, Comment
# from blog_api.serializers.serializers import CategorySerializer


# # View for listing and creating categories
# class CategoryListCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     pagination_class = StandardResultsSetPagination

#     def get(self, request):
#         """
#         Retrieve all categories with pagination.
#         """
#         try:
#             categories = Category.objects.all().order_by('id')  # Order the queryset
#             paginator = self.pagination_class()
#             result_page = paginator.paginate_queryset(categories, request)
#             serializer = CategorySerializer(result_page, many=True)
#             return paginator.get_paginated_response(serializer.data)
#         except Exception as e:
#             return Response({
#                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 'message': str(e)
#             })
    
#     def post(self, request):
#         """
#         Create a new category.
#         """
#         serializer = CategorySerializer(data=request.data)
#         try:
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({
#                     'status': status.HTTP_201_CREATED,
#                     'message': 'Category created successfully',
#                     'data': serializer.data
#                 })
#             return Response({
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': serializer.errors
#             })

#         except Exception as e:
#             return Response({
#                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 'message': str(e)
#             })
import logging
from blog_api.pagination import StandardResultsSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import IntegrityError
from blog_api.models import Category
from blog_api.serializers.serializers import CategorySerializer
from blog_api.permissions import WriterPermission, ReadOnlyPermission


logger = logging.getLogger(__name__)

class CategoryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, WriterPermission | ReadOnlyPermission]   
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        """
        Retrieve all categories with pagination.
        """
        try:
            categories = Category.objects.all().order_by('id')  # Order the queryset
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(categories, request)
            serializer = CategorySerializer(result_page, many=True)
            logger.info("Retrieve all categories")
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving blogs categories {str(e)}")
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """
        Create a new category.
        """
        serializer = CategorySerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                logger.info("Created category entry successfully")
                return Response({
                    'message': 'Category created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
                logger.warning(f"Invalid data for creating blog post: {serializer.errors}")
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error creating blog categories: {str(e)}")
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
