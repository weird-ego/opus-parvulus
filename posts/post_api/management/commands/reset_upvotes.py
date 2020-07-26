from django.core.management.base import BaseCommand

from post_api.models import Post, Upvote


class Command(BaseCommand):
    help = "reset upvotes"

    def handle(self, *args, **kwargs):
        queryset = Post.objects.all()
        queryset.update(upvotes=0)
        Upvote.objects.all().delete()
