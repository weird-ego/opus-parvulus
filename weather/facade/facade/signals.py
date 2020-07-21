from os import environ

from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from requests.exceptions import ConnectionError


from .models import WeatherState

dashboard_url = environ['dashboard_url']


@receiver(post_save, sender=WeatherState)
def notify_dashboard(sender, instance, **kwargs):
    try:
        response = requests.post(url=f"http://{dashboard_url}/notify/{instance.city.id}")
        if response.text != "ok":
            raise Exception("failed to notify dashboard")
    except ConnectionError:
        pass  # notify server is offline
