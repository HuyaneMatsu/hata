import vampytest

from ....user import User

from ..fields import put_users


def _iter_options():
    user_id_0 = 202209150004
    
    user_0 = User.precreate(user_id_0)
    
    yield (
        [],
        False,
        {
            'recipients': [],
        },
    )
    
    yield (
        [],
        True,
        {
            'recipients': [],
        },
    )
    
    yield (
        [user_0],
        False,
        {
            'recipients': [
                user_0.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        [user_0],
        True,
        {
            'recipients': [
                user_0.to_data(defaults = True, include_internals = True),
            ],
        },
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_users(input_value, defaults):
    """
    Tests whether ``put_users`` is working as intended.
    
    Parameters
    ----------
    input_value : `list<ClientUserBase>`
        Value to serialise.
    defaults : `bool`
        Whether default values should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_users(input_value, {}, defaults)
