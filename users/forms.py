from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils.safestring import mark_safe
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import FormActions, StrictButton

# from crispy_bootstrap5.bootstrap5 import FloatingField


class LoginForm(BaseForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        required=True, max_length=100, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id="login-form")
        self.set_next_url()
        self.create_layout(
            Layout(
                FloatingField("email", autocomplete="email"),
                FloatingField("password", autocomplete="current-password"),
                FormActions(
                    StrictButton(
                        mark_safe("Login"),
                        type="submit",
                        name="action",
                        value="login",
                        css_class="button button-small w-100 my-3 text-center",
                    )
                ),
            )
        )

    def clean_password(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        if not password or not email:
            return None
        user = authenticate(
            self.request,
            username=email.lower(),
            password=password,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        err = None
        if not user:
            err = "Incorrect Email or Password!"
        elif not user.affiliate_user:
            err = "Please register for the affiliate program using the form below."
        if err:
            self.raise_validation_error("password", password, err)
        return user

    def process(self):
        data = {}
        is_valid = self.is_valid()
        post_data = self.request.POST
        is_ajax = "ajax" in post_data
        if not is_valid:
            if not is_ajax:
                return None
            errors = {}
            for field, error in self.errors.items():
                errors[field] = error[0]
            data["errors"] = errors
        cleaned_data = self.cleaned_data
        user = cleaned_data.get("password") if is_valid else None
        if user:
            next_url = cleaned_data.get(auth_next_var)
            log_user(self.request, user)
            login(
                self.request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
            return HttpResponseRedirect(
                next_url or reverse("hoi:affiliate_dashboard_home")
            )
        if is_ajax:
            return JsonResponse(data)
        return None
