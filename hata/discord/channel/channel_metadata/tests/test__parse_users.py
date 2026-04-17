import vampytest

from ....user import User

from ..fields import parse_users


def _iter_options():
    user_id_0 = 202209150000
    user_id_1 = 202209150001
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield (
        {},
        [],
    )
    yield (
        {
            'recipients': [],
        },
        [],
    )
    yield (
        {
            'recipients': [
                user_0.to_data(defaults = True, include_internals = True),
                user_1.to_data(defaults = True, include_internals = True),
            ],
        },
        [user_0, user_1],
    )
    yield (
        {
            'recipients': [
                user_1.to_data(defaults = True, include_internals = True),
                user_0.to_data(defaults = True, include_internals = True),
            ],
        },
        [user_0, user_1],
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
    output : `list<ClientUserBase>`
    """
    return parse_users(input_data)
