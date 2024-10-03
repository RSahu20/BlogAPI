


# # from django.test import TestCase
# # from django.contrib.auth.models import User
# # from blog_api.models import Comment, Tag, Post, Category
# # from blog_api.serializers import CommentSerializer, PostSerializer, serializers

# # # class PostSerializerTest(TestCase):

# import pytest
# from rest_framework import status
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User
# from django.urls import reverse
# from blog_api.models import Category, Tag, Post, Comment

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def user(api_client):
#     user = User.objects.create_user(username='testuser', password='testpass')
#     api_client.force_authenticate(user=user)
#     return user

# @pytest.fixture
# def category_and_tag():
#     category = Category.objects.create(name='Tech')
#     tag = Tag.objects.create(name='Python')
#     return category, tag

# @pytest.mark.django_db
# def test_category_list_create(api_client, user):
#     # Test listing categories
#     url = reverse('blog-category')  # Make sure this URL name matches your urls.py
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK

#     # Test creating a new category
#     data = {'name': 'Lifestyle'}
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['message'] == 'Category created successfully'

# @pytest.mark.django_db
# def test_tag_list_create(api_client, user):
#     # Test listing tags
#     url = reverse('blog-tag')  # Make sure this URL name matches your urls.py
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK

#     # Test creating a new tag
#     data = {'name': 'Django'}
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['message'] == 'Tag created successfully'

# @pytest.mark.django_db
# def test_post_list_create(api_client, user, category_and_tag):
#     category, tag = category_and_tag
#     # Test listing posts
#     url = reverse('blog-post')
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK

#     # Test creating a new post
#     data = {
#         'title': 'Test Post',
#         'content': 'This is a test post.',
#         'category': category.id,
#         'tags': [tag.id]
#     }
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['message'] == 'Blog entry created successfully'

# @pytest.mark.django_db
# def test_comment_list_create(api_client, user, category_and_tag):
#     category, tag = category_and_tag
#     post = Post.objects.create(
#         title='Test Post',
#         content='This is a test post.',
#         category=category
#     )
#     # Test listing comments
#     url = reverse('blog-comment')
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK

#     # Test creating a new comment
#     data = {
#         'post': post.id,
#         'content': 'This is a test comment.'
#     }
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data['message'] == 'Comment added successfully'

# @pytest.mark.django_db
# def test_single_comment(api_client, user, category_and_tag):
#     category, tag = category_and_tag
#     post = Post.objects.create(
#         title='Test Post',
#         content='This is a test post.',
#         category=category
#     )
#     comment = Comment.objects.create(
#         post=post,
#         author=user,
#         content='This is a test comment.'
#     )
#     # Test retrieving a single comment
#     url = reverse('single-comment', args=[comment.id])
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['message'] == 'Retrieve comment successfully'

#     # Test updating a single comment
#     data = {'content': 'Updated comment content.'}
#     response = api_client.put(url, data, format='json')
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['message'] == 'Comment updated successfully'
#     assert response.data['data']['content'] == 'Updated comment content.'

#     # Test deleting a single comment
#     response = api_client.delete(url)
#     assert response.status_code == status.HTTP_204_NO_CONTENT

# @pytest.mark.django_db
# def test_single_post(api_client, user, category_and_tag):
#     category, tag = category_and_tag
#     post = Post.objects.create(
#         title='Test Post',
#         content='This is a test post.',
#         category=category
#     )
#     # Test retrieving a single post
#     url = reverse('single-blog-post', args=[post.id])
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK

#     # Test updating a single post
#     data = {
#         'title': 'Updated Post Title',
#         'content': 'Updated content.',
#         'category': category.id,
#         'tags': [tag.id]
#     }
#     response = api_client.put(url, data, format='json')
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['message'] == 'Post updated successfully'
#     assert response.data['data']['title'] == 'Updated Post Title'

#     # Test deleting a single post
#     response = api_client.delete(url)
#     assert response.status_code == status.HTTP_204_NO_CONTENT

