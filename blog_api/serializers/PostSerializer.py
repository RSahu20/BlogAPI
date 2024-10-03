from ..models import Tag, Category, Post, Comment
from rest_framework import serializers
from django.contrib.auth.models import User
from blog_api.serializers.serializers import CategorySerializer,TagSerializer

class PostSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'tags']
    
    # def create(self, validated_data):
    #     category_data = validated_data.pop('category')
    #     tags_data = validated_data.pop('tags')
    #     category = Category.objects.get(id=category_data['id'])
    #     post = Post.objects.create(category=category, **validated_data)
    #     for tag_data in tags_data:
    #         tag = Tag.objects.get(id=tag_data['id'])
    #         post.tags.add(tag)
    #     return post

    # def update(self, instance, validated_data):
    #     category_data = validated_data.pop('category')
    #     tags_data = validated_data.pop('tags')
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.content = validated_data.get('content', instance.content)
    #     # instance.author = validated_data.get('author', instance.author)
    #     instance.category = Category.objects.get(id=category_data['id'])
    #     instance.tags.clear()
    #     for tag_data in tags_data:
    #         tag = Tag.objects.get(id=tag_data['id'])
    #         instance.tags.add(tag)
    #     instance.save()
    #     return instance