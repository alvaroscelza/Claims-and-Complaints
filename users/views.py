from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .token import account_activation_token, account_password_reset_token
from users.forms import (
    LoginForm,
    RegisterForm,
    ChangePasswordForm,
    ChangeProfilePictureForm,
    ForgotPasswordForm,
)


# Create your views here.
@login_required
def profile(request):
    base_form_args = {
        "request": request,
        "action": reverse("users:profile"),
    }
    change_password_form = change_profile_picture_form = None
    if request.method == "POST":
        action = request.POST.get("action")
        response = None
        if action == "updatepassword":
            change_password_form = ChangePasswordForm(request.POST, **base_form_args)
            response = change_password_form.process()
        elif action == "updateprofilepicture":
            change_profile_picture_form = ChangeProfilePictureForm(
                request.POST, request.FILES, **base_form_args
            )
            change_profile_picture_form.process()
        if response:
            return response
    context = {
        "change_password_form": change_password_form
        or ChangePasswordForm(**base_form_args),
        "change_profile_picture_form": change_profile_picture_form
        or ChangeProfilePictureForm(**base_form_args),
    }
    return render(request, "users/dashboard/profile.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    register_form = None
    base_form_args = {
        "request": request,
        "action": reverse("users:register"),
    }
    if request.method == "POST":
        register_form = RegisterForm(request.POST, **base_form_args)
        response = register_form.process()
        if response:
            return response
    context = {"form": register_form or RegisterForm(**base_form_args)}
    return render(request, "users/register.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
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


def forgot_password(request, user_id=None, token=None):
    if (
        request.user.is_authenticated
        or (user_id and not token)
        or (not user_id and token)
    ):
        return redirect("home")
    user = forgot_form = None
    if user_id:
        user = get_object_or_404(get_user_model(), id=user_id)
    is_token_valid = (
        account_password_reset_token.check_token(user_id, token) if user else False
    )
    base_form_args = {
        "request": request,
        "action": reverse(
            "users:forgot_password",
            kwargs={"token": token, "user_id": user_id} if is_token_valid else {},
        ),
    }
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "forgottenpassword":
            forgot_form = ForgotPasswordForm(request.POST, **base_form_args)
            response = forgot_form.process()
        elif action == "updatepassword":
            if not user or not is_token_valid:
                messages.error("Invalid Request")
                return redirect("users:forgot_password")
            change_form = ChangePasswordForm(request.POST, **base_form_args)
            response = change_form.process(user=user)
        if response:
            return response
    context = {
        "form": (forgot_form or ForgotPasswordForm(**base_form_args))
        if not is_token_valid
        else (change_form or ChangePasswordForm(**base_form_args))
    }
    return render(request, "users/forgot_password.html", context)


def verify_email(request, user_id, token):
    user = get_object_or_404(get_user_model(), id=user_id)
    is_valid = account_activation_token.check_token(user, token)
    if is_valid:
        user.email_validated = timezone.now()
        messages.success("Welcome! Account Verified Successfully!")
    else:
        messages.warning("Invalid Request, Please try again!")
    return redirect("users:login")
