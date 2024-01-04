from django import forms
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError
from django.utils import dateparse
from crispy_forms.layout import Field, Layout

auth_next_var = "next"  # Used in url's to determine the next page to be redirected to


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        form_tag = kwargs.pop("use_form_tag", True)
        form_css_class = kwargs.pop("form_css_class", "")
        form_action = kwargs.pop("action")
        r = kwargs.pop("request", None)
        if r:
            self.request = r
        form_id = kwargs.pop("id", None)

        self.track = None
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = form_tag
        if form_tag:
            self.helper.form_action = form_action
            self.helper.form_class = "loading-wrap" + (
                " " + form_css_class if form_css_class else ""
            )
            if form_id:
                self.helper.form_id = form_id
        # self.helper.reneder_hidden_fields = True
        # self.helper.render_required_fields = True

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
        data = {"htmlUpdate": [], "collapse": [], "addClass": []}
        if not valid and is_xhr:
            errors = {}
            for field, error in self.errors.items():
                if field == "contact_number":
                    field = "contact_number_1"
                errors[field] = error[0]
            data["errors"] = errors
        self.process_default(data, is_valid=valid)
        if valid:
            ret = self.process_valid(data, action=self.data.get("action"))
            if ret:
                return ret

    def raise_validation_error(self, field, value, msg="This field is required."):
        raise ValidationError(msg, params={field: value}, code="invalid")

    def parse_date(self, date):
        return dateparse.parse_datetime((date).strip('"'))

    def form_add_class(self, css_class):
        self.helper.form_class += " " + css_class

    def render_crispy_layout(self, layout):
        hp = FormHelper()
        hp.form_tag = False
        hp.layout = layout
        return render_crispy_form(self, hp)

    def validate_full_name(self, field, required_field=None):
        name = self.cleaned_data[field]
        required = required_field and self.cleaned_data.get(required_field)
        if required and not name:
            raise ValidationError(
                "This field is required.", params={field: name}, code="invalid"
            )
        if name and name.count(" ") < 1:
            raise ValidationError(
                "Please enter your Full Name", params={field: name}, code="invalid"
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
                "This field is required.", params={field: value}, code="invalid"
            )
        return self.cleaned_data[field]

    def set_next_url(self):
        if not self.request:
            return None
        next_url = (
            self.request.POST.get(auth_next_var)
            if self.request.method == "POST"
            else (
                self.request.GET.get("next") if self.request.method == "GET" else None
            )
        )
        if not next_url:
            return None
        self.fields[auth_next_var] = forms.CharField(
            initial=next_url, widget=forms.HiddenInput
        )
