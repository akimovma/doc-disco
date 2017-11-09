from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User, CustomerProfile
from .validators import validate_phone


class CustomerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(label='Phone number',
                                   max_length=15,
                                   validators=[validate_phone], required=False)
    address = forms.CharField(label='Address', max_length=100, required=False)
    accepted_agreement = forms.BooleanField(label='Accept User Agreement')
    hear_us_from = forms.CharField(label='Where did you hear about us?', widget=forms.Textarea, required=False)
    customer_type = forms.ChoiceField(label='Who you are?', choices=CustomerProfile.CUSTOMER_TYPE)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone_number', 'address',
                  'accepted_agreement', 'hear_us_from', 'customer_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None
        for field_name in ['first_name', 'last_name']:
            self.fields[field_name].required = True

    def clean(self):
        cleaned_data = super().clean()
        profile = {
            'phone_number': cleaned_data.pop('phone_number', ''),
            'address': cleaned_data.pop('address', ''),
            'accepted_agreement': cleaned_data.pop('accepted_agreement', False),
            'hear_us_from': cleaned_data.pop('hear_us_from', ''),
            'customer_type': cleaned_data.pop('customer_type'), }
        cleaned_data['profile'] = profile
        return cleaned_data


class CreateClerkForm(UserCreationForm):
    phone_number = forms.CharField(label='Phone number',
                                   max_length=15,
                                   validators=[validate_phone], required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        profile = {
            'phone_number': cleaned_data.pop('phone_number', ''),
        }
        cleaned_data['profile'] = profile
        return cleaned_data
