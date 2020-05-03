from django.db import IntegrityError

class InsufficientBalance(IntegrityError):
    """Raised when a user has an insufficient balance to purchase"""