import vampytest

from ....user import User

from ...embedded_activity_user_state import EmbeddedActivityUserState

from ..fields import parse_user_states


def _iter_options():
    guild_id = 202409010090
    
    embedded_activity_user_state_0 = EmbeddedActivityUserState(user = User.precreate(202409010091))
    embedded_activity_user_state_1 = EmbeddedActivityUserState(user = User.precreate(202409010092))
    
    yield (
        {
            'participants': None,
        },
        guild_id,
        {},
    )
    
    yield (
        {
            'participants': [],
        },
        guild_id,
        {},
    )
    
    yield (
        {
            'participants': [
                embedded_activity_user_state_0.to_data(guild_id = guild_id),
                embedded_activity_user_state_1.to_data(guild_id = guild_id),
            ],
        },
        guild_id,
        {
            embedded_activity_user_state_0.user_id: embedded_activity_user_state_0,
            embedded_activity_user_state_1.user_id: embedded_activity_user_state_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_user_states(input_data, guild_id):
    """
    Tests whether ``parse_user_states`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `dict<int, EmbeddedActivityUserState>`
    """
    user_states = {}
    output = parse_user_states(input_data, user_states, guild_id)
    vampytest.assert_instance(output, dict)
    vampytest.assert_is(output, user_states)
    return output
