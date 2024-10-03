from django.urls import path
from blog_api.views.CategoryView import CategoryListCreateView
from blog_api.views.CommentView import CommentListCreateView,SingleCommentView
from blog_api.views.TagsView import TagListCreateView
from blog_api.views.BlogView import BlogListCreateView,SingleBlogView



urlpatterns = [
    path('blog/', BlogListCreateView.as_view(), name='blog-post'),  # List and create blog posts
    path('blog/<int:id>/', SingleBlogView.as_view(), name='single-blog-post'),  # Retrieve, update, or delete a single blog post
    path('tag/', TagListCreateView.as_view(), name='blog-tag'),  # List and create tags
    path('category/', CategoryListCreateView.as_view(), name='blog-category'),  # List and create categories
    path('comment/', CommentListCreateView.as_view(), name='blog-comment'),  # List and create comments
    path('comment/<int:id>/', SingleCommentView.as_view(), name='single-comment')  # Retrieve, update, or delete a single comment
]
