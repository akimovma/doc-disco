from django.core.exceptions import ValidationError
from django.conf import settings

import re


def validate_phone(value):
    reg = re.compile(settings.PHONE_REGEX)
    if not reg.match(value):
        raise ValidationError("Phone number must be entered in the format: '+999999999'."
                              "Up to 15 digits allowed.")
