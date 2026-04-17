__all__ = ()


# expire grace period
EXPIRE_GRACE_PERIOD_DEFAULT = 0

EXPIRE_GRACE_PERIOD_OPTIONS = frozenset((
    EXPIRE_GRACE_PERIOD_DEFAULT,
    1, 3, 7, 14, 30
))

# subscriber count
SUBSCRIBER_COUNT_DEFAULT = 0
