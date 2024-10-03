# from django.test import TestCase
# from django.contrib.auth.models import User
# from blog_api.models import Category, Tag, Post, Comment

# class BlogModelTests(TestCase):
    
#     def setUp(self):
#         # Create a user for testing
#         self.user = User.objects.create_user(username='testuser', password='12345')

#         # Create a category for testing
#         self.category = Category.objects.create(name='Test Category')

#         # Create a tag for testing
#         self.tag = Tag.objects.create(name='Test Tag')

#         # Create a post for testing
#         self.post = Post.objects.create(
#             title='Test Post',
#             content='This is a test post content.',
#             category=self.category,
#         )
#         self.post.tags.add(self.tag)

#         # Create a comment for testing
#         self.comment = Comment.objects.create(
#             post=self.post,
#             author=self.user,
#             content='This is a test comment.'
#         )
    
#     def test_category_creation(self):
#         self.assertEqual(str(self.category), 'Test Category')
    
#     def test_tag_creation(self):
#         self.assertEqual(str(self.tag), 'Test Tag')
    
#     def test_post_creation(self):
#         self.assertEqual(str(self.post), 'Test Post')
#         self.assertEqual(self.post.content, 'This is a test post content.')
#         self.assertEqual(self.post.category.name, 'Test Category')
#         self.assertIn(self.tag, self.post.tags.all())

#     def test_comment_creation(self):
#         self.assertEqual(str(self.comment), 'This is a test comment.')
#         self.assertEqual(self.comment.post, self.post)
#         self.assertEqual(self.comment.author, self.user)

