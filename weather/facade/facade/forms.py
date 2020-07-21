from django import forms

from . import models


class SubscriptionForm(forms.Form):
    city_id = forms.IntegerField()
