from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import FormActions, StrictButton
from config.base_forms import BaseForm, auth_next_var
from crispy_bootstrap5.bootstrap5 import FloatingField


class LoginForm(BaseForm):
    username = forms.CharField(required=True)
    password = forms.CharField(
        required=True, max_length=100, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id="login-form")
        self.set_next_url()
        self.create_layout(
            Layout(
                FloatingField("username", autocomplete="username"),
                FloatingField("password", autocomplete="current-password"),
                FormActions(
                    StrictButton(
                        mark_safe("Login"),
                        type="submit",
                        name="action",
                        value="login",
                        css_class="btn btn-success w-100 my-3 text-center",
                    )
                ),
            )
        )

    def clean_password(self):
        # Returns user object if valid
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        if not password or not username:
            return None
        user = authenticate(
            self.request,
            username=username,
            password=password,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        err = None
        if not user:
            err = "Incorrect Email or Password!"
        if err:
            self.raise_validation_error("password", password, err)
        return user

    def process(self):
        is_valid = self.is_valid()
        cleaned_data = self.cleaned_data
        user = cleaned_data.get("password") if is_valid else None
        if not user:
            # Return form with error
            return None
        next_url = cleaned_data.get(auth_next_var)
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect(next_url or "home")
