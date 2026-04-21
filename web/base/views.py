from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

from .forms import LoginForm


def _redirect(name: str) -> HttpResponseRedirect:
    return HttpResponseRedirect(reverse(name))


def home(request: HttpRequest) -> HttpResponse:
    return TemplateResponse(
        request,
        "base/index.html",
        {
            "form": LoginForm(),
            "login_failed": False,
        },
    )


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return _redirect("base:dashboard")

    form = LoginForm(request.POST or None)
    login_failed = False

    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            return _redirect("base:dashboard")
        login_failed = True

    return TemplateResponse(
        request,
        "base/index.html",
        {
            "form": form,
            "login_failed": login_failed,
        },
    )


def logout_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        logout(request)
    return _redirect("base:home")


def dashboard(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return _redirect("base:login")

    return TemplateResponse(
        request,
        "base/dashboard.html",
        {},
    )
