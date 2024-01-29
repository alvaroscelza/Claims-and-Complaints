from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from crispy_forms.layout import HTML
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import dateparse
from django.utils.safestring import mark_safe

auth_next_var = 'next'


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        form_tag = kwargs.pop('use_form_tag', True)
        form_css_class = kwargs.pop('form_css_class', '')
        form_action = kwargs.pop('action')
        r = kwargs.pop('request', None)
        if r:
            self.request = r
        form_id = kwargs.pop('id', None)

        self.track = None
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = form_tag
        if form_tag:
            self.helper.form_action = form_action
            self.helper.form_class = 'loading-wrap' + (
                ' ' + form_css_class if form_css_class else ''
            )
            if form_id:
                self.helper.form_id = form_id

    def process_default(self, data: dict, is_valid):
        # A function to be overridden which is run regardless of valid or invalid
        pass

    def process_valid(self, data: dict, action: str):
        # A function which is run if the form data is valid
        pass

    def process(self):
        valid = self.is_valid()
        is_xhr = (
            False  # Detect if this request is from javascript or not (not implemented)
        )
        errors = None
        data = {'htmlUpdate': [], 'collapse': [], 'addClass': []}
        if not valid and is_xhr:
            errors = {}
            for field, error in self.errors.items():
                if field == 'contact_number':
                    field = 'contact_number_1'
                errors[field] = error[0]
            data['errors'] = errors
        self.process_default(data, is_valid=valid)
        if valid:
            ret = self.process_valid(data, action=self.data.get('action'))
            if ret:
                return ret

    def raise_validation_error(self, field, value, msg='This field is required.'):
        raise ValidationError(msg, params={field: value}, code='invalid')

    def parse_date(self, date):
        return dateparse.parse_datetime((date).strip('"'))

    def form_add_class(self, css_class):
        self.helper.form_class += ' ' + css_class

    def validate_full_name(self, field, required_field=None):
        name = self.cleaned_data[field]
        required = required_field and self.cleaned_data.get(required_field)
        if required and not name:
            raise ValidationError(
                'This field is required.', params={field: name}, code='invalid'
            )
        if name and name.count(' ') < 1:
            raise ValidationError(
                'Please enter your Full Name', params={field: name}, code='invalid'
            )
        return name

    def create_layout(
        self,
        layout,
        base_layout=None,
    ):
        # Template_vars Used for placing any data or tracking
        template_vars = Layout(
            Field(auth_next_var) if auth_next_var in self.fields else None,
            base_layout,
        )
        layout = Layout(template_vars, layout)
        self.helper.layout = layout

    def validate_is_required(self, condition, field, can_validate=True):
        value = self.cleaned_data[field]
        if can_validate and self.cleaned_data[condition] and not value:
            raise ValidationError(
                'This field is required.', params={field: value}, code='invalid'
            )
        return self.cleaned_data[field]

    def set_next_url(self):
        if not self.request:
            return None
        next_url = (
            self.request.POST.get(auth_next_var)
            if self.request.method == 'POST'
            else (
                self.request.GET.get('next') if self.request.method == 'GET' else None
            )
        )
        if not next_url:
            return None
        self.fields[auth_next_var] = forms.CharField(
            initial=next_url, widget=forms.HiddenInput
        )


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
                HTML(f'<a href="{reverse("accounts:forgot_password")}">Forgotten your Password?</a>')
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
            resend_verification_email_link = reverse('accounts:login_resend', kwargs={'resend_user_id': user.id})
            anchor = f'<a href="{resend_verification_email_link}">Resend Email</a>'
            error = mark_safe(f'Please Validate your account from the email we sent, {anchor}')  # nosec
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
            login_anchor = f'<a href="{reverse("accounts:login")}">Log In</a>'
            error_message = f'An account already exists with this email, Please {login_anchor}'
            self.raise_validation_error('email', email, mark_safe(error_message))  # nosec
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
        return redirect('accounts:login')


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
        return redirect('accounts:profile')


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
        return redirect('accounts:profile')


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
        return redirect('accounts:login')
