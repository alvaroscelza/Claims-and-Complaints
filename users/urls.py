from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("signup/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path(
        "forgot-password/<int:user_id>/<token>/",
        views.forgot_password,
        name="forgot_password",
    ),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify/<int:user_id>/<token>", views.verify_email, name="verify_email"),
]
# login, register, profile,logout
