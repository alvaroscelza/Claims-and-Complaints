from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.layout import Layout, HTML
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect
from django.urls import reverse

from config.base_forms import BaseForm, auth_next_var


class LoginForm(BaseForm):
    username = forms.EmailField(required=True, label='Email')
    password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id='login-form')
        self.set_next_url()
        self.create_layout(
            Layout(
                FloatingField('username', autocomplete='username'),
                FloatingField('password', autocomplete='current-password'),
                HTML(f'<a href="{reverse("users:forgot_password")}">Forgotten your Password?</a>')
                if self.request.method == 'POST'
                else Layout(),
                FormActions(
                    StrictButton('Login', type='submit', name='action', value='login',
                                 css_class='btn btn-success w-100 my-3 text-center')
                ),
            )
        )

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not password or not username:
            return None
        backend = 'django.contrib.auth.backends.ModelBackend'
        user = authenticate(self.request, username=username, password=password, backend=backend)
        error = None
        if not user:
            error = 'Incorrect Username or Password!'
        elif not user.email_validated:
            resend_verification_email_link = reverse('users:login_resend', kwargs={'resend_user_id': user.id})
            anchor = f'<a href="{resend_verification_email_link}">Resend Email</a>'
            error = f'Please Validate your account from the email we sent, {anchor}'
        if error:
            self.raise_validation_error('password', password, error)
        return user

    def process(self):
        is_valid = self.is_valid()
        cleaned_data = self.cleaned_data
        user = cleaned_data.get('password') if is_valid else None
        if not user:
            return None
        next_url = cleaned_data.get(auth_next_var)
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(next_url or 'home')


class RegisterForm(BaseForm):
    email = forms.EmailField(required=True, label='Your Email')
    new_password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id='register-form')
        self.set_next_url()

        self.create_layout(
            Layout(
                FloatingField('email', autocomplete='email'),
                FloatingField('new_password', autocomplete='new-password'),
                FloatingField('confirm_new_password', autocomplete='new-password'),
                FormActions(
                    StrictButton('Sign Up', type='submit', name='action', value='register',
                                 css_class='btn btn-success w-100 my-3 text-center')
                ),
            )
        )

    def clean_name(self):
        return self.validate_full_name('name')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user_exists = get_user_model().objects.filter(email=email).exists()
        if user_exists:
            login_anchor = f'<a href="{reverse("users:login")}">Log In</a>'
            error_message = f'An account already exists with this email, Please {login_anchor}'
            self.raise_validation_error('email', email, error_message)
        return email

    def clean_confirm_new_password(self):
        password = self.cleaned_data.get('new_password')
        conf_password = self.cleaned_data['confirm_new_password']
        if not password and not conf_password:
            return None
        if password != conf_password:
            self.raise_validation_error('confirm_new_password', conf_password, 'Passwords do not match!')
        return password

    def process(self):
        is_valid = self.is_valid()
        if not is_valid:
            return None
        cleaned_data = self.cleaned_data
        email = cleaned_data['email']
        name = cleaned_data['name'].split(' ') if 'name' in cleaned_data else ['', '']
        user = get_user_model().objects.create(email=email, first_name=name[0], last_name=name[-1], username=email)
        user.set_password(cleaned_data['confirm_new_password'])
        user.save()
        user.send_verification_email(request=self.request)
        success_message = 'Account created successfully, Please verify your account from the email we sent!'
        messages.success(self.request, success_message)
        return redirect('users:login')


class ChangePasswordForm(BaseForm):
    new_password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id='forgot-password-form')
        self.set_next_url()
        self.create_layout(
            Layout(
                FloatingField('new_password', autocomplete='new-password'),
                FloatingField('confirm_new_password', autocomplete='new-password'),
                FormActions(
                    StrictButton('Update Password', type='submit', name='action', value='updatepassword',
                                 css_class='btn btn-success w-100 my-3 text-center')
                ),
            )
        )

    def clean_confirm_new_password(self):
        password = self.cleaned_data.get('new_password')
        conf_password = self.cleaned_data['confirm_new_password']
        if not password and not conf_password:
            return None
        if password != conf_password:
            self.raise_validation_error('confirm_new_password', conf_password, 'Passwords do not match!')
        return password

    def process(self, user=None):
        if not user and not self.request.user.is_authenticated:
            return None
        is_valid = self.is_valid()
        user = user or self.request.user
        if not is_valid:
            return None
        cleaned_data = self.cleaned_data
        user.set_password(cleaned_data['confirm_new_password'])
        user.save()
        messages.success(self.request, 'Password updated successfully! Please login.')
        return redirect('users:profile')


class ChangeProfilePictureForm(BaseForm):
    image = forms.ImageField(required=True, label='New Profile Picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id='change-profilepic-form')
        self.set_next_url()
        self.create_layout(
            Layout(
                'image',
                FormActions(
                    StrictButton('Upload Image', type='submit', name='action', value='updateprofilepicture',
                                 css_class='btn btn-success w-100 my-3 text-center')
                ),
            )
        )

    def process(self):
        is_valid = self.is_valid()
        user = self.request.user
        if not is_valid or not user.is_authenticated:
            return None
        user.profile_picture = self.cleaned_data['image']
        user.save()
        messages.success(self.request, 'Profile Picture Updated Successfully!')
        return redirect('users:profile')


class ForgotPasswordForm(BaseForm):
    email = forms.EmailField(
        required=True,
        label='Your Email',
        help_text='If an account exists we will send you a recovery email!',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, id='change-profilepic-form')
        self.set_next_url()
        self.create_layout(
            Layout(
                'email',
                FormActions(
                    StrictButton('Recover', type='submit', name='action', value='forgottenpassword',
                                 css_class='btn btn-success w-100 my-3 text-center')
                ),
            )
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = get_user_model().objects.filter(email=email).first()
        if not user:
            self.raise_validation_error('email', email, 'No account found')
        return user

    def process(self):
        is_valid = self.is_valid()
        if not is_valid:
            return None
        user = self.cleaned_data['email']
        user.send_forgot_password_email(request=self.request)
        messages.success(self.request, 'We have sent an email. Use the link to reset your password!')
        return redirect('users:login')
