import vampytest

from ....user import User, GuildProfile

from ...interaction_event import InteractionEvent

from ..fields import put_users_into


def _iter_options():
    user_id = 202211050023
    guild_id = 202211050024
    user_name = 'Faker'
    user_nick = 'COLORS'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    guild_profile = GuildProfile(nick = user_nick)
    user.guild_profiles[guild_id] = guild_profile
    
    interaction_event_instance = InteractionEvent(guild_id = guild_id)
    
    
    yield (
        None,
        False,
        None,
        {},
    )
    
    yield (
        None,
        True,
        None,
        {
            'users': {},
            'members': {},
        },
    )
    
    yield (
        {
            user_id: user,
        },
            False,
            None,
        {
            'users': {
                str(user_id): user.to_data(defaults = False, include_internals = True),
            },
            'members': {},
        },
    )
    
    yield (
        {
            user_id: user,
        },
            False,
            interaction_event_instance,
        {
            'users': {
                str(user_id): user.to_data(defaults = False, include_internals = True),
            },
            'members': {
                str(user_id): guild_profile.to_data(defaults = False, include_internals = True),
            },
        },
    )
    
    yield (
        {
            user_id: user,
        },
            True,
            None,
        {
            'users': {
                str(user_id): user.to_data(defaults = True, include_internals = True),
            },
            'members': {},
        },
    )
    
    yield (
        {
            user_id: user,
        },
            True,
            interaction_event_instance,
        {
            'users': {
                str(user_id): user.to_data(defaults = True, include_internals = True),
            },
            'members': {
                str(user_id): guild_profile.to_data(defaults = True, include_internals = True),
            },
        },
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_users_into(input_value, defaults, interaction_event):
    """
    Tests whether ``put_users_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, ClientUserBase>`
        Value to serialise.
    defaults : `bool`
        Whether default values should be serialised as well.
    interaction_event : `None | InteractionEvent`
        The respective interaction event.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_users_into(input_value, {}, defaults, interaction_event = interaction_event)
