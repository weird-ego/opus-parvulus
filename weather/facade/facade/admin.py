from django.contrib import admin

from . import models

admin.site.register(models.WeatherState)
admin.site.register(models.City)
admin.site.register(models.Weather)
