from django.urls import path

from . import views


urlpatterns = [
    path('index/', views.Index.as_view(), name='index'),
    path('signout/', views.SignOut.as_view(), name='signout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('cities/', views.Cities.as_view(), name='cities'),
    path('subscription/', views.Subscription.as_view(), name='subscription'),
    path('weather_state/', views.WeatherState.as_view(), name='weather_state')
]
