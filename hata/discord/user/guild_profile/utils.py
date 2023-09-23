__all__ = ()

from datetime import datetime as DateTime
from functools import partial as partial_func
from warnings import warn

from ..voice_state.fields import (
    put_channel_id_into, put_deaf_into, put_mute_into, validate_channel_id, validate_deaf, validate_mute
)

from .fields import (
    put_nick_into, put_role_ids_into, put_timed_out_until_into, validate_nick, validate_role_ids,
    validate_timed_out_until, validate_timeout_duration
)
from .guild_profile import GUILD_PROFILE_AVATAR


def validate_timeout_duration_with_deprecation(timeout_duration):
    """
    Validates the given `timeout_duration`, but also accepts `DateTime` and `None` as before.
    
    Deprecated and will be removed in 2024 March.
    
    Parameters
    ----------
    timeout_duration : `None`, `DateTime`, `int`, `TimeDelta`, `float`
        Timeout duration.
    
    Returns
    -------
    timed_out_until : `None`, `DateTime`
    
    Raises
    ------
    TypeError
    """
    if (timeout_duration is None) or isinstance(timeout_duration, DateTime):
        warn(
            (
                f'`timeout_duration` parameter cannot be `None`, {DateTime.__name__}; '
                f'please use `timed_out_until` parameter instead. '
                f'This warning will be removed at 2024 March and `TypeError` will be propagated instead.'
            ),
            FutureWarning,
            stacklevel = 4,
        )
        
        return validate_timed_out_until(timeout_duration)
    
    return validate_timeout_duration(timeout_duration)


GUILD_PROFILE_FIELD_CONVERTERS = {
    'deaf': (validate_deaf, put_deaf_into),
    'mute': (validate_mute, put_mute_into),
    'nick': (validate_nick, put_nick_into),
    'role_ids': (validate_role_ids, put_role_ids_into),
    'roles': (validate_role_ids, put_role_ids_into),
    'timed_out_until': (validate_timed_out_until, put_timed_out_until_into),
    'timeout_duration': (validate_timeout_duration_with_deprecation, put_timed_out_until_into),
    'voice_channel': (validate_channel_id, put_channel_id_into),
    'voice_channel_id': (validate_channel_id, put_channel_id_into),
}

GUILD_PROFILE_SELF_FIELD_CONVERTERS = {
    'avatar': (
        partial_func(GUILD_PROFILE_AVATAR.validate_icon, allow_data = True),
        partial_func(GUILD_PROFILE_AVATAR.put_into, as_data = True),
    ),
    'nick': (validate_nick, put_nick_into),
}
