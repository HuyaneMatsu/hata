import vampytest

from ....user import User

from ..fields import put_target_user_into


def _iter_options():
    user = User.precreate(202308030004, name = 'Ken')
    
    yield None, True, {'target_user': None}
    yield None, False, {}
    
    yield user, True, {'target_user': user.to_data(defaults = True, include_internals = True)}
    yield user, False, {'target_user': user.to_data(defaults = False, include_internals = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_user_into(input_value, defaults):
    """
    Tests whether ``put_target_user_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | ClientUserBase`
        Input value to serialize.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target_user_into(input_value, {}, defaults)
