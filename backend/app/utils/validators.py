"""Reusable Pydantic-compatible validators."""
import re

PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")


def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))


def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_letter and has_digit
