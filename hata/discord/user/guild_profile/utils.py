__all__ = ()

from functools import partial as partial_func

from ..voice_state.fields import (
    put_channel_id, put_deaf, put_mute, validate_channel_id, validate_deaf, validate_mute
)

from .fields import (
    put_avatar_decoration, put_nick, put_role_ids, put_timed_out_until, validate_avatar_decoration,
    validate_nick, validate_role_ids, validate_timed_out_until, validate_timeout_duration
)
from .guild_profile import GUILD_PROFILE_AVATAR, GUILD_PROFILE_BANNER


GUILD_PROFILE_FIELD_CONVERTERS = {
    'deaf': (validate_deaf, put_deaf),
    'mute': (validate_mute, put_mute),
    'nick': (validate_nick, put_nick),
    'role_ids': (validate_role_ids, put_role_ids),
    'roles': (validate_role_ids, put_role_ids),
    'timeout_duration': (validate_timeout_duration, put_timed_out_until),
    'timed_out_until': (validate_timed_out_until, put_timed_out_until),
    'voice_channel': (validate_channel_id, put_channel_id),
    'voice_channel_id': (validate_channel_id, put_channel_id),
}

GUILD_PROFILE_SELF_FIELD_CONVERTERS = {
    'avatar': (
        partial_func(GUILD_PROFILE_AVATAR.validate_icon, allow_data = True),
        partial_func(GUILD_PROFILE_AVATAR.put_into, as_data = True),
    ),
    'avatar_decoration': (validate_avatar_decoration, put_avatar_decoration),
    'banner': (
        partial_func(GUILD_PROFILE_BANNER.validate_icon, allow_data = True),
        partial_func(GUILD_PROFILE_BANNER.put_into, as_data = True),
    ),
    'nick': (validate_nick, put_nick),
}
