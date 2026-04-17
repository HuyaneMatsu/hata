import vampytest

from ...guild_widget_user import GuildWidgetUser

from ..fields import put_users


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
        None,
        False,
        {
            'members': [],
        },
    )
    
    yield (
        None,
        True,
        {
            'members': [],
        },
    )
    
    yield (
        (user_0, user_1),
        False,
        {
            'members': [
                user_0.to_data(defaults = False),
                user_1.to_data(defaults = False),
            ],
        },
    )
    
    yield (
        (user_0, user_1),
        True,
        {
            'members': [
                user_0.to_data(defaults = True),
                user_1.to_data(defaults = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_users(input_value, defaults):
    """
    Tests whether ``put_users`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<GuildWidgetUser>`
        Value to serialise.
    defaults : `bool`
        Whether default values should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_users(input_value, {}, defaults)
