from django.core.management.base import BaseCommand


from facade.models import City


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        names = [
            'london', 'toronto', 'tokyo', 'berlin', 'moscow',
            'NY', 'kyiv', 'paris', 'cairo', 'rome', 'beijing',
        ]
        for name in names:
            City.objects.get_or_create(name=name)
