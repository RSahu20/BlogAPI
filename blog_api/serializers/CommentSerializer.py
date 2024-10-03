
from blog_api. models import Tag, Category, Post, Comment
from rest_framework import serializers
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    # blog_title = serializers.SerializerMethodField()
    # author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = "__all__"

    # def get_blog_title(self, obj):
    #     return obj.post.title

    # def get_author_name(self, obj):
    #     return obj.author.username