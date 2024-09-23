from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Albom, BlogPost, Comment, Like


class AlbumeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Albom
        fields = "__all__"


# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
#     username = serializers.CharField(source='user.username', read_only=True)
#     post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)
#     reply = serializers.CharField(read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ['user', 'username', 'text', 'post', 'reply']
#
#     def get_replies(self, comment):
#         serializer = CommentSerializer(comment.replies.all(), many=True)
#         return serializer.data


class LikeSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    # username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ["user", "is_liked", "post"]


#
class PostSerializer(serializers.ModelSerializer):
    # post_author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    # author = serializers.CharField(source='post_author.username', read_only=True)
    # comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BlogPost
        # fields = ['text', 'author', 'post_author', 'likes_count', 'comments']
        fields = [
            "text",
            "category",
            "title",
            "likes_count",
        ]
        # fields = [ 'user', 'likes_count']

    #     def create(self, validated_data):
    #         post_author = validated_data.pop('post_author')
    #         post = BlogPost.objects.create(post_author=post_author, **validated_data)
    #         return post

    def get_likes_count(self, obj):
        like_count = Like.objects.filter(post=obj).count()
        return like_count

    # @extend_schema_field(str)
    # def get_comments(self, obj):
    #     # comments=Comment.objects.filter(post=obj)
    #     comments = Comment.objects.filter(post=obj).all()
    #     serializer = CommentSerializer(comments, many=True)
    #     return serializer.data
