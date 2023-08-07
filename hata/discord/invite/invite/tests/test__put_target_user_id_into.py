import vampytest

from ..fields import put_target_user_id_into


def _iter_options():
    user_id = 202308060052
    
    yield 0, False, {}
    yield 0, True, {'target_user_id': None}
    yield user_id, False, {'target_user_id': str(user_id)}
    yield user_id, True, {'target_user_id': str(user_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_user_id_into(input_value, defaults):
    """
    Tests whether ``put_target_user_id_into`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target_user_id_into(input_value, {}, defaults)
