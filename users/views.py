from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.urls import reverse

from users.forms import LoginForm


# Create your views here.
def profile(request):
    pass


def register(request):
    pass


def login(request):
    login_form = None
    base_form_args = {
        "request": request,
        "action": reverse("users:login"),
    }
    if request.method == "POST":
        login_form = LoginForm(request.POST, **base_form_args)
        response = login_form.process()
        if response:
            return response
    context = {"form": login_form or LoginForm(**base_form_args)}
    return render(request, "users/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("home")
