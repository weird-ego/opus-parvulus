from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS


class CheckAuthor:
    def create(self, request, *args, **kwargs):
        if request.user.username != request.POST["author_name"]:
            return Response(
                {"status": "fail", "errors": ["Wrong author_name"]}, status=403
            )
        return super().create(request, *args, **kwargs)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
