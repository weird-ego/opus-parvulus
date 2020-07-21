from os import environ

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        admin, created = User.objects.get_or_create(username=environ['admin_name'],
                                                    password=environ['admin_pass'])
        if created:
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
