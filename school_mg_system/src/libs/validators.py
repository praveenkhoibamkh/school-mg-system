import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .constants import PASSWORD_REGEX


def validate_mail(email: str) -> bool:
    try:
        validate_email(email)
    except ValidationError:
        return False
    return True


def validate_password(password: str) -> bool:
    return True  # if re.fullmatch(PASSWORD_REGEX, password) is not None else False
