import vampytest

from ....user import User

from ..fields import put_user


def _iter_options():
    user = User.precreate(202405010001, name = 'Yuuka')
    
    yield user, True, {'user': user.to_data(defaults = True, include_internals = True)}
    yield user, False, {'user': user.to_data(defaults = False, include_internals = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user(input_value, defaults):
    """
    Tests whether ``put_user`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ClientUserBase``
        Input value to serialize.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_user(input_value, {}, defaults)
