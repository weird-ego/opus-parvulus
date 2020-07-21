from django.db import models, transaction, connection
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class WeatherUser(User):
    class Meta:
        proxy = True


class Weather(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __repr__(self):
        return f"Weather(name={self.name})"

    __str__ = __repr__


try:
    NO_WEATHER = Weather.objects.get(name="no data")
except Weather.DoesNotExist:
    NO_WEATHER = Weather.objects.create(name="no data")
except:
    NO_WEATHER = None  # no migrations yet


class City(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __repr__(self):
        return f"City(name={self.name})"

    __str__ = __repr__

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            global NO_WEATHER
            if NO_WEATHER is None:
                NO_WEATHER = Weather.objects.create(name="no data")
            ws = WeatherState(city=self, weather=NO_WEATHER)
            ws.save()


class WeatherState(models.Model):
    db_table = 'weather_state'

    city = models.OneToOneField(City,
                                on_delete=models.CASCADE,
                                related_name='weather')
    weather = models.ForeignKey(Weather,
                                on_delete=models.CASCADE)
    temperature = models.IntegerField(default=0)

    def __repr__(self):
        return (f"WeatherState(city={self.city.name},"
                f" weather={self.weather.name}, temperature="
                f"{self.temperature})")

    __str__ = __repr__


class Subscription(models.Model):
    db_table = 'subscription'

    user = models.ForeignKey(WeatherUser, on_delete=models.CASCADE)
    weather_state = models.ForeignKey(WeatherState,
                                         on_delete=models.CASCADE,
                                         related_name='subscription')

    @classmethod
    def from_user_and_city_id(cls, user, city_id):
        with transaction.atomic():
            weather_state = WeatherState.objects.get(city__id=city_id)
            instance = cls(
                user=user,
                weather_state=weather_state
            )
            instance.save()
            return instance

    class Meta:
        unique_together = ('user', 'weather_state')
