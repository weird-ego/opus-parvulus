from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, CommentViewSet, RelatedCommentsList, UpvoteView


root = routers.DefaultRouter()
root.register(r"posts", PostViewSet)
root.register(r"comments", CommentViewSet)

urlpatterns = [
    path("upvote/<int:pid>/", UpvoteView.as_view()),
    path("", include(root.urls)),
    path("related_comments/<int:pid>/", RelatedCommentsList.as_view()),
]
