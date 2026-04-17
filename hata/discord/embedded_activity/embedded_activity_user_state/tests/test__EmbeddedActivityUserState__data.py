import vampytest

from ....user import GuildProfile, User

from ..constants import SESSION_ID_LENGTH_MIN
from ..embedded_activity_user_state import EmbeddedActivityUserState

from .test__EmbeddedActivityUserState__constructor import _assert_fields_set


def test__EmbeddedActivityUserState__from_data():
    """
    Tests whether ``EmbeddedActivityUserState.from_data`` works as intended.
    """
    guild_id = 202409010014
    
    nonce = 'miau'
    session_id = 'a' * SESSION_ID_LENGTH_MIN
    user = User.precreate(202409010015)
    guild_profile = GuildProfile(nick = 'sinker')
    user.guild_profiles[guild_id] = guild_profile
    
    data = {
        'nonce': nonce,
        'session_id': session_id,
        'member': {
            **guild_profile.to_data(include_internals = True),
            'user': user.to_data(include_internals = True),
        },
        'user_id': str(user.id),
    }
    
    embedded_activity_user_state = EmbeddedActivityUserState.from_data(data, guild_id)
    _assert_fields_set(embedded_activity_user_state)
    
    vampytest.assert_eq(embedded_activity_user_state.nonce, nonce)
    vampytest.assert_eq(embedded_activity_user_state.session_id, session_id)
    vampytest.assert_is(embedded_activity_user_state.user, user)


def test__EmbeddedActivityUserState__to_data():
    """
    Tests whether ``EmbeddedActivityUserState.to_data`` works as intended.
    """
    guild_id = 202409010016
    
    nonce = 'miau'
    session_id = 'a' * SESSION_ID_LENGTH_MIN
    user = User.precreate(202409010017)
    guild_profile = GuildProfile(nick = 'sinker')
    user.guild_profiles[guild_id] = guild_profile
    
    data = {
        'nonce': nonce,
        'session_id': session_id,
        'member': {
            **guild_profile.to_data(defaults = True, include_internals = True),
            'user': user.to_data(defaults = True, include_internals = True),
        },
        'user_id': str(user.id),
    }
    
    embedded_activity_user_state = EmbeddedActivityUserState(
        nonce = nonce,
        session_id = session_id,
        user = user,
    )
    vampytest.assert_eq(
        embedded_activity_user_state.to_data(defaults = True, guild_id = guild_id),
        data,
    )
