from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("signup/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
# login, register, profile,logout
