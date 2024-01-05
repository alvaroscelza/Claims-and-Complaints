from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import FormActions, StrictButton
from config.base_forms import BaseForm, auth_next_var
from crispy_bootstrap5.bootstrap5 import FloatingField


class LoginForm(BaseForm):
    username = forms.CharField(required=True)
    # username = forms.EmailField(required=True,label="Email")
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
            err = "Incorrect Username or Password!"
        elif not user.email_validated:
            err = mark_safe(
                'Please Validate your account from the email we sent, <a href="\#">Resend Email</a>'
            )
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


class RegisterForm(BaseForm):
    name = forms.CharField(required=True, max_length=100, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email")
    new_password = forms.CharField(
        required=True, max_length=100, widget=forms.PasswordInput
    )
    confirm_new_password = forms.CharField(
        required=True, max_length=100, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id="register-form")
        self.set_next_url()

        self.create_layout(
            Layout(
                FloatingField("name", autocomplete="name"),
                FloatingField("email", autocomplete="email"),
                FloatingField("new_password", autocomplete="new-password"),
                FloatingField("confirm_new_password", autocomplete="new-password"),
                FormActions(
                    StrictButton(
                        mark_safe("Sign Up"),
                        type="submit",
                        name="action",
                        value="register",
                        css_class="btn btn-success w-100 my-3 text-center",
                    )
                ),
            )
        )

    def clean_name(self):
        return self.validate_full_name("name")

    def clean_email(self):
        # Check if email exists
        email = self.cleaned_data["email"].lower()
        # Check for existing user:
        user_exists = get_user_model().objects.filter(email=email).exists()
        if user_exists:
            self.raise_validation_error(
                "email",
                email,
                mark_safe(
                    f'An account already exists with this email, Please <a href="{reverse("users:login")}">Log In</a>'
                ),
            )
        return email

    def clean_confirm_new_password(self):
        # Verify passwords match
        password = self.cleaned_data.get("new_password")
        conf_password = self.cleaned_data["confirm_new_password"]
        if not password and not conf_password:
            return None
        if password != conf_password:
            self.raise_validation_error(
                "confirm_new_password",
                conf_password,
                mark_safe("Passwords do not match!"),
            )
        return password

    def process(self):
        is_valid = self.is_valid()
        if not is_valid:
            return None
        cleaned_data = self.cleaned_data
        email = cleaned_data["email"]
        name = cleaned_data["name"].split(" ")

        user = get_user_model().objects.create(
            email=email,
            first_name=name[0],
            last_name=name[-1],
            username=email,
        )

        # if settings.DEBUG:
        #     user.email_validated = timezone.now()
        user.set_password(cleaned_data["confirm_new_password"])
        user.save()
        messages.success(
            self.request,
            "Account created successfully, Please verify your account from the email we sent!",
        )
        return redirect("users:login")


class ChangePasswordForm(BaseForm):
    new_password = forms.CharField(
        required=True, max_length=100, widget=forms.PasswordInput
    )
    confirm_new_password = forms.CharField(
        required=True, max_length=100, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id="forgot-password-form")
        self.set_next_url()
        self.create_layout(
            Layout(
                FloatingField("new_password", autocomplete="new-password"),
                FloatingField("confirm_new_password", autocomplete="new-password"),
                FormActions(
                    StrictButton(
                        mark_safe("Update Password"),
                        type="submit",
                        name="action",
                        value="updatepassword",
                        css_class="btn btn-success w-100 my-3 text-center",
                    )
                ),
            )
        )

    def clean_confirm_new_password(self):
        # Verify passwords match
        password = self.cleaned_data.get("new_password")
        conf_password = self.cleaned_data["confirm_new_password"]
        if not password and not conf_password:
            return None
        if password != conf_password:
            self.raise_validation_error(
                "confirm_new_password",
                conf_password,
                mark_safe("Passwords do not match!"),
            )
        return password

    def process(self):
        is_valid = self.is_valid()
        user = self.request.user
        if not is_valid or not user.is_authenticated:
            return None
        cleaned_data = self.cleaned_data
        user.set_password(cleaned_data["confirm_new_password"])
        user.save()
        messages.success(
            self.request,
            "Password updated successfully! Please login.",
        )
        return redirect("users:profile")


class ChangeProfilePictureForm(BaseForm):
    image = forms.ImageField(required=True, label="New Profile Picture")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id="change-profilepic-form")
        self.fields["image"].default = "test..."
        self.set_next_url()
        self.create_layout(
            Layout(
                "image",
                FormActions(
                    StrictButton(
                        mark_safe("Upload Image"),
                        type="submit",
                        name="action",
                        value="updateprofilepicture",
                        css_class="btn btn-success w-100 my-3 text-center",
                    )
                ),
            )
        )

    def process(self):
        is_valid = self.is_valid()
        user = self.request.user
        if not is_valid or not user.is_authenticated:
            return None
        user.profile_picture = self.cleaned_data["image"]
        user.save()
        messages.success(
            self.request,
            "Profile Picture Updated Successfully!",
        )
        return redirect("users:profile")


class ForgotPasswordForm(BaseForm):
    email = forms.EmailField(
        required=True,
        label="Your Email",
        help_text="If an account exists we will send you a recovery email!",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id="change-profilepic-form")
        self.fields["image"].default = "test..."
        self.set_next_url()
        self.create_layout(
            Layout(
                "email",
                FormActions(
                    StrictButton(
                        mark_safe("Recover"),
                        type="submit",
                        name="action",
                        value="forgottenpassword",
                        css_class="btn btn-success w-100 my-3 text-center",
                    )
                ),
            )
        )

    def process(self):
        is_valid = self.is_valid()
        user = self.request.user
        if not is_valid or not user.is_authenticated:
            return None
        user.profile_picture = self.cleaned_data["image"]
        user.save()
        messages.success(
            self.request,
            "Profile Picture Updated Successfully!",
        )
        return redirect("users:profile")
