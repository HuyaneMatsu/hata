import vampytest

from ...guild_widget_user import GuildWidgetUser

from ..fields import parse_users


def _iter_options():
    user_id_0 = 10
    user_name_0 = 'Far'
    
    user_id_1 = 11
    user_name_1 = 'East'
    
    user_0 = GuildWidgetUser(
        user_id = user_id_0,
        name = user_name_0,
    )
    
    user_1 = GuildWidgetUser(
        user_id = user_id_1,
        name = user_name_1,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'members': None,
        },
        None,
    )
    
    yield (
        {
            'members': [],
        },
        None,
    )
    
    yield (
        {
            'members': [
                user_0.to_data(),
            ],
        },
        (user_0,),
    )
    
    yield (
        {
            'members': [
                user_0.to_data(),
                user_1.to_data(),
            ],
        },
        (user_0, user_1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_users(input_data):
    """
    Tests whether ``parse_users`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | list<GuildWidgetUser>`
    """
    return parse_users(input_data)
