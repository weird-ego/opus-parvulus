from django.urls import path

from .views import IndexView, SignView, SignoutView, PostView


urlpatterns = [
    path("sign/", SignView.as_view(), name="sign"),
    path("signout/", SignoutView.as_view(), name="signout"),
    path("post/<int:pid>", PostView.as_view(), name="post"),
    path("", IndexView.as_view(), name="index"),
]
