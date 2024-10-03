from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import check_password
from .models import UserPasswordHistory

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Password must be at least 8 characters long."),
                code='password_too_short',
            )
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code='password_no_digit',
            )
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code='password_no_uppercase',
            )
        if not any(char in "!@#$%^&*()_+" for char in password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )
        
        previous_passwords = UserPasswordHistory.objects.filter(user=user)
        for entry in previous_passwords:
            if check_password(password, entry.password):
                raise ValidationError(
                    _("Password cannot be the same as any of your previous passwords."),
                    code='password_reused',
                )

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long, contain at least one digit, one uppercase letter, and one special character."
        )
