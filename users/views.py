from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.
def profile(request):
    pass


def register(request):
    pass


def login(request):
    if request.method == "POST":
        raise Exception("Not configured")
    form = None
    context = {"form": form}
    return render(request, "users/login.html", context)


def logout(request):
    logout(request)
    return redirect("home")
