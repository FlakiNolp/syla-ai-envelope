from dataclasses import dataclass
import email_validator

from domain.exceptions.email import EmailValidationException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Email(BaseValueObject):
    value: str

    def validate(self):
        try:
            email_validator.validate_email(self.value)
        except email_validator.EmailSyntaxError:
            raise EmailValidationException(text=self.value)

    def as_generic_type(self):
        return str(self.value)
