from django.views import View
from django.http import JsonResponse
from django.db.transaction import atomic
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, Comment, Upvote
from .serializers import PostSerializer, CommentSerializer
from .utils import CheckAuthor, ReadOnly


class PostViewSet(CheckAuthor, viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("id")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(CheckAuthor, viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("id")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RelatedCommentsList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [ReadOnly]

    def get_queryset(self):
        pid = self.kwargs["pid"]
        return Comment.objects.filter(post__id=pid)


class UpvoteView(LoginRequiredMixin, View):
    def post(self, request, pid):
        post = Post.objects.get(pk=pid)
        user = request.user
        with atomic():
            upvote, created = Upvote.objects.get_or_create(
                user=user,
                post=post
            )
            if created:
                post.upvotes += 1
                post.save()
                return JsonResponse({"status": "ok"})
        return JsonResponse({"status": "fail", "error": ["Already upvoted"]})
