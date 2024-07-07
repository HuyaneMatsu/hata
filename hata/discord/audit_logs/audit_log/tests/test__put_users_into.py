import vampytest

from ....user import User

from ..fields import put_users_into


def _iter_options():
    user_id_0 = 202406250015
    user_id_1 = 202406250016
    
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'users': [],
        },
    )
    
    yield (
        {
            user_id_0: user_0,
            user_id_1: user_1,
        },
        False,
        {
            'users': [
                user_0.to_data(defaults = False, include_internals = True),
                user_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        {
            user_id_0: user_0,
            user_id_1: user_1,
        },
        True,
        {
            'users': [
                user_0.to_data(defaults = True, include_internals = True),
                user_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_users_into(input_value, defaults):
    """
    Tests whether ``put_users_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, User>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_users_into(input_value, {}, defaults)
