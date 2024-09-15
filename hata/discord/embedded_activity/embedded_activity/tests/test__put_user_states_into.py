import vampytest

from ....user import User

from ...embedded_activity_user_state import EmbeddedActivityUserState

from ..fields import put_user_states_into


def _iter_options():
    guild_id = 202409010093
    
    embedded_activity_user_state_0 = EmbeddedActivityUserState(user = User.precreate(202409010094))
    embedded_activity_user_state_1 = EmbeddedActivityUserState(user = User.precreate(202409010095))
    
    yield (
        {},
        False,
        guild_id,
        {
            'participants': [],
        },
    )
    
    yield (
        {},
        True,
        guild_id,
        {
            'participants': [],
        },
    )
    
    yield (
        {
            embedded_activity_user_state_0.user_id: embedded_activity_user_state_0,
            embedded_activity_user_state_1.user_id: embedded_activity_user_state_1,
        },
        False,
        guild_id,
        {
            'participants': [
                embedded_activity_user_state_0.to_data(defaults = False, guild_id = guild_id),
                embedded_activity_user_state_1.to_data(defaults = False, guild_id = guild_id),
            ],
        },
    )
    
    yield (
        {
            embedded_activity_user_state_0.user_id: embedded_activity_user_state_0,
            embedded_activity_user_state_1.user_id: embedded_activity_user_state_1,
        },
        True,
        guild_id,
        {
            'participants': [
                embedded_activity_user_state_0.to_data(defaults = True, guild_id = guild_id),
                embedded_activity_user_state_1.to_data(defaults = True, guild_id = guild_id),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user_states_into(input_value, defaults, guild_id):
    """
    Tests whether ``put_user_states_into`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<int, EmbeddedActivityUserState>`
        Data to parse from.
    defaults : `bool`
        Whether fields with their default value should be included.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_user_states_into(input_value, {}, defaults, guild_id = guild_id)
