__all__ = ()

from functools import partial as partial_func

from ..voice_state.fields import (
    put_channel_id_into, put_deaf_into, put_mute_into, validate_channel_id, validate_deaf, validate_mute
)

from .fields import (
    put_avatar_decoration_into, put_nick_into, put_role_ids_into, put_timed_out_until_into, validate_avatar_decoration,
    validate_nick, validate_role_ids, validate_timed_out_until, validate_timeout_duration
)
from .guild_profile import GUILD_PROFILE_AVATAR, GUILD_PROFILE_BANNER


GUILD_PROFILE_FIELD_CONVERTERS = {
    'deaf': (validate_deaf, put_deaf_into),
    'mute': (validate_mute, put_mute_into),
    'nick': (validate_nick, put_nick_into),
    'role_ids': (validate_role_ids, put_role_ids_into),
    'roles': (validate_role_ids, put_role_ids_into),
    'timeout_duration': (validate_timeout_duration, put_timed_out_until_into),
    'timed_out_until': (validate_timed_out_until, put_timed_out_until_into),
    'voice_channel': (validate_channel_id, put_channel_id_into),
    'voice_channel_id': (validate_channel_id, put_channel_id_into),
}

GUILD_PROFILE_SELF_FIELD_CONVERTERS = {
    'avatar': (
        partial_func(GUILD_PROFILE_AVATAR.validate_icon, allow_data = True),
        partial_func(GUILD_PROFILE_AVATAR.put_into, as_data = True),
    ),
    'avatar_decoration': (validate_avatar_decoration, put_avatar_decoration_into),
    'banner': (
        partial_func(GUILD_PROFILE_BANNER.validate_icon, allow_data = True),
        partial_func(GUILD_PROFILE_BANNER.put_into, as_data = True),
    ),
    'nick': (validate_nick, put_nick_into),
}
