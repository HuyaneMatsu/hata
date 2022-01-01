__all__ = ()

from scarletio import IgnoreCaseString


AUDIT_LOG_REASON = IgnoreCaseString('X-Audit-Log-Reason')

RATE_LIMIT_REMAINING = IgnoreCaseString('X-RateLimit-Remaining')
RATE_LIMIT_RESET = IgnoreCaseString('X-RateLimit-Reset')
RATE_LIMIT_RESET_AFTER = IgnoreCaseString('X-RateLimit-Reset-After')
RATE_LIMIT_LIMIT = IgnoreCaseString('X-RateLimit-Limit')

# to send
RATE_LIMIT_PRECISION = IgnoreCaseString('X-RateLimit-Precision')
DEBUG_OPTIONS = IgnoreCaseString('X-Debug-Options')
