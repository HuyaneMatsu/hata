import vampytest

from ....user import User, GuildProfile

from ...interaction_event import InteractionEvent

from ..fields import parse_users


def _iter_options():
    user_id_0 = 202211050025
    guild_id_0 = 202211050026
    
    user_id_1 = 202310050002
    guild_id_1 = 202310050003
    
    user_name = 'Faker'
    user_nick = 'COLORS'
    
    user_0 = User.precreate(
        user_id_0,
        name = user_name,
    )
    
    user_1 = User.precreate(
        user_id_1,
        name = user_name,
    )
    
    interaction_event_0 = InteractionEvent(guild_id = guild_id_0)
    interaction_event_1 = InteractionEvent(guild_id = guild_id_1)
    
    guild_profile = GuildProfile(nick = user_nick)
    
    yield (
        {},
        interaction_event_0,
        None,
    )
    
    yield (
        {
            'users': {},
        },
        interaction_event_0,
        None,
    )
    
    yield (
        {
            'users': {},
            'members': {},
        },
        interaction_event_0,
        None,
    )
    
    yield (
        {
            'members': {},
        },
        interaction_event_0,
        None,
    )
    
    yield (
        {
            'users': {
                str(user_id_0): user_0.to_data(defaults = True, include_internals = True),
            }
        },
        interaction_event_0,
        (
            {
                user_id_0: user_0,
            },
            [None],
        ),
    )
    
    yield (
        {
            'users': {
                str(user_id_1): user_1.to_data(defaults = True, include_internals = True),
            },
            'members': {
                 str(user_id_1): guild_profile.to_data(defaults = True, include_internals = True),
            },
        },
        interaction_event_1,
        (
            {
                user_id_1: user_1,
            },
            [
                guild_profile,
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_users(input_data, interaction_event):
    """
    Tests whether ``parse_users`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    interaction_event : ``InteractionEvent``
        Respective interaction event received with the users.
    
    Returns
    -------
    output : `None | (dict<int, ClientUserBase>, list<GuildProfile>)`
    """
    output = parse_users(input_data, interaction_event)
    if output is not None:
        output = (
            output,
            [user.guild_profiles.get(interaction_event.guild_id) for user in output.values()],
        )
    
    return output
