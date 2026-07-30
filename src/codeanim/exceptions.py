class CodeAnimError(Exception):
    """Base exception for all codeanim errors."""


class AbortedError(CodeAnimError):
    """Raised when execution is aborted via the abort key."""
