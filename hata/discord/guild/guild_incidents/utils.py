__all__ = ()

from .fields import (
    put_direct_messages_disabled_until, put_invites_disabled_until,
    validate_direct_messages_disabled_duration, validate_direct_messages_disabled_until,
    validate_invites_disabled_duration, validate_invites_disabled_until
)


GUILD_INCIDENTS_FIELD_CONVERTERS = {
    'validate_direct_messages_disabled_duration': (
        validate_direct_messages_disabled_duration, put_direct_messages_disabled_until,
    ),
    'direct_messages_disabled_until': (
        validate_direct_messages_disabled_until, put_direct_messages_disabled_until,
    ),
    'invites_disabled_duration': (validate_invites_disabled_duration, put_invites_disabled_until),
    'invites_disabled_until': (validate_invites_disabled_until, put_invites_disabled_until),
}
