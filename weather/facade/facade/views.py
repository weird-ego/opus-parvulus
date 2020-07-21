from django import http
from django.db.models import Q
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout, forms
from django.contrib.auth.mixins import LoginRequiredMixin


from . import models
from .utils import csrf_protect_class
from .forms import SubscriptionForm


class Index(TemplateView):
    template_name = 'facade/index.html'


@csrf_protect_class
class SignIn(View):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        status = user is not None
        if status:
            login(request, user)
            return http.HttpResponse('ok')
        return http.HttpResponseForbidden()


@csrf_protect_class
class SignUp(View):

    def post(self, request):
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return http.HttpResponse('ok')
        return http.HttpResponseBadRequest(str(form.errors))


@csrf_protect_class
class SignOut(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request):
        logout(request)
        return http.HttpResponse('ok')


class Cities(LoginRequiredMixin, ListView):
    model = models.City
    response_class = http.JsonResponse

    def render_to_response(self, context, **response_kwargs):
        raw_data = context['object_list']
        data = {'cities':  [{'name': city.name, 'id': city.id} for city in raw_data]}
        return self.response_class(data)


@csrf_protect_class
class Subscription(LoginRequiredMixin, View):

    def post(self, request):
        objects = models.Subscription.objects.filter(user=request.user)
        if objects.count() == 5:
            return http.JsonResponse({})
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            city_id = form.cleaned_data['city_id']
            user = request.user
            subscription = models.Subscription.from_user_and_city_id(
                user,
                city_id
            )
            subscription.save()
            data = {
                'city_name': subscription.weather_state.city.name,
                'weather': subscription.weather_state.weather.name,
                'temperature': subscription.weather_state.temperature,
                'id': subscription.id
            }
            return http.JsonResponse(data)
        return http.JsonResponse(form.errors)

    def delete(self, request):
        qs = http.QueryDict(request.META['QUERY_STRING'])
        subscription_id = int(qs['subscription_id'])
        subscription = models.Subscription.objects.get(pk=subscription_id)
        subscription.delete()
        return http.HttpResponse('ok')


class WeatherState(LoginRequiredMixin, ListView):
    model = models.WeatherState
    response_class = http.JsonResponse
    selected_fields = 'city__name', 'weather__name', 'subscription', 'temperature'

    def get_queryset(self):
        user = self.request.user
        objects = self.model.objects
        return objects.filter(subscription__user=user)

    def render_to_response(self, context, **response_kwargs):
        raw_data = context['object_list']
        data = raw_data.values(*self.selected_fields)
        return self.response_class({'weather_state': list(data)})
