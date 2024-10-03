import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blog_api.models import Category, Tag, Post, Comment
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestBlogAPI:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
    
        self.category = Category.objects.create(name='Tech')
        self.tag = Tag.objects.create(name='Python')
        
        self.post_data = {
            'title': 'Post Title',
            'content': 'Content of the post.',
            'category': self.category.id,
            'tags': [self.tag.id]
        }
        
        self.update_post_data = {
            'title': 'Updated Post Title',
            'content': 'Updated content of the post.',
            'category': self.category.id,
            'tags': [self.tag.id]
        }
        
        self.post = Post.objects.create(
            title='Initial Post Title',
            content='Initial content.',
            category=self.category
        )
        self.post.tags.add(self.tag)
        
        self.comment_data = {
            'post': self.post.id,
            'author': self.user.id,
            'content': 'This is a test comment.'
        }
        
        self.update_comment_data = {
            'post':self.post.id,
            'author':self.user.id,
            'content': 'This is an updated test comment.'
        }
        
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Initial comment.'
        )

    # Post Tests
    def test_create_post(self):
        response = self.client.post(reverse('blog-post'), self.post_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 2
        assert Post.objects.latest('id').title == 'Post Title'

    def test_retrieve_post(self):
        response = self.client.get(reverse('single-blog-post', args=[self.post.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['title'] == 'Initial Post Title'

    def test_update_post(self):
        response = self.client.put(reverse('single-blog-post', args=[self.post.id]), self.update_post_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.post.refresh_from_db()
        assert self.post.title == 'Updated Post Title'

    def test_delete_post(self):
        initial_count = Post.objects.count()
        response = self.client.delete(reverse('single-blog-post', args=[self.post.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Post.objects.count() == initial_count - 1  # Assuming one post left

    def test_list_posts(self):
        response = self.client.get(reverse('blog-post'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1  # Assuming one post initially

    # Comment Tests
    def test_create_comment(self):
        response = self.client.post(reverse('blog-comment'), self.comment_data, format='json')
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == 2
        assert Comment.objects.latest('id').content == 'This is a test comment.'

    def test_retrieve_comment(self):
        response = self.client.get(reverse('single-comment', args=[self.comment.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['content'] == 'Initial comment.'

    def test_update_comment(self):
        response = self.client.put(reverse('single-comment', args=[self.comment.id]), self.update_comment_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.comment.refresh_from_db()
        assert self.comment.content == 'This is an updated test comment.'

    def test_delete_comment(self):
        initial_count = Comment.objects.count()
        response = self.client.delete(reverse('single-comment', args=[self.comment.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Comment.objects.count() == initial_count-1  # Assuming one comment left

    def test_list_comments(self):
        response = self.client.get(reverse('blog-comment'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1 

    # Category Tests
    def test_create_category(self):
        response = self.client.post(reverse('blog-category'), {'name': 'New Category'}, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 2
        assert Category.objects.latest('id').name == 'New Category'

    def test_retrieve_category(self):
        response = self.client.get(reverse('blog-category'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1 

   

    def test_list_categories(self):
        response = self.client.get(reverse('blog-category'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1 

    # Tag Tests
    def test_create_tag(self):
        response = self.client.post(reverse('blog-tag'), {'name': 'New Tag'}, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Tag.objects.count() == 2
        assert Tag.objects.latest('id').name == 'New Tag'

    def test_retrieve_tag(self):
        response = self.client.get(reverse('blog-tag'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1  


    def test_list_tags(self):
        response = self.client.get(reverse('blog-tag'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1 
