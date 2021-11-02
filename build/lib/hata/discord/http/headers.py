__all__ = ()

from ...backend.utils import istr

AUDIT_LOG_REASON = istr('X-Audit-Log-Reason')

RATE_LIMIT_REMAINING = istr('X-RateLimit-Remaining')
RATE_LIMIT_RESET = istr('X-RateLimit-Reset')
RATE_LIMIT_RESET_AFTER = istr('X-RateLimit-Reset-After')
RATE_LIMIT_LIMIT = istr('X-RateLimit-Limit')

# to send
RATE_LIMIT_PRECISION = istr('X-RateLimit-Precision')
DEBUG_OPTIONS = istr('X-Debug-Options')
