class HousingError(Exception):
    """Base exception for service-layer failures."""


class HousingValidationError(HousingError):
    """Raised when business rules are violated."""


class HousingNotFoundError(HousingError):
    """Raised when a requested object cannot be found."""
