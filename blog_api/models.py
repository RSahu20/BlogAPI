from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'blogs_category'

    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'blog_tags'
    

class Post(models.Model):
    """ Blog model for various blog info and fields"""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name='Blog Title' )
    # author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    updated_at = models.DateField(auto_now = True)   
    created_at = models.DateField(auto_now_add = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    """ add comment fields within comment model to manage blog comments"""

    post = models.ForeignKey(Post,related_name='comments', on_delete= models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

