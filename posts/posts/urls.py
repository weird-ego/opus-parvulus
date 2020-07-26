from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("post_app.urls")),
    path("api/", include("post_api.urls")),
    path("admin/", admin.site.urls),
]
