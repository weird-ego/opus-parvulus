from django.core.management.base import BaseCommand
from requests import get


from facade.models import Weather, WeatherState, City


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = 'http://wttr.in/{city}\?format="%C:%t"'
        for city in City.objects.all():
            response = get(url.format(city=city.name))
            if response.ok:
                text = response.content.decode().strip('"')
                weather, temperature = text.split(':')
                temperature = int(temperature[:-2])
                weather, _ = Weather.objects.get_or_create(name=weather)
                weather_state = city.weather
                weather_state.weather = weather
                weather_state.temperature = temperature
                weather_state.save()
