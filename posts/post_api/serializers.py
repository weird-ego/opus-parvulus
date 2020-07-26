from .models import Post, Comment
from rest_framework.serializers import ModelSerializer


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id", "title", "link", "creation_date",
            "upvotes", "author_name"
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author_name", "content", "creation_date"]
