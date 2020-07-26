from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render


class IndexView(TemplateView):
    template_name = "index.html"


class PostView(TemplateView):
    template_name = "post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_auth"] = self.request.user.is_authenticated
        context["pid"] = kwargs["pid"]
        context["author"] = self.request.user.username
        return context


class SignView(View):
    def get(self, request):
        return render(request, "sign.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            login(request, user)
            return redirect("index")
        except IntegrityError:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return redirect("sign")


class SignoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("index")
