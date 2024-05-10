import vampytest

from ..fields import put_failed_user_ids_into


def _iter_options():
    user_id_0 = 202405010022
    user_id_1 = 202405010023
    
    yield None, False, {'failed_users': []}
    yield None, True, {'failed_users': []}
    yield (user_id_0, user_id_1,), False, {'failed_users': [str(user_id_0), str(user_id_1)]}
    yield (user_id_0, user_id_1,), True, {'failed_users': [str(user_id_0), str(user_id_1)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_failed_user_ids_into(input_value, defaults):
    """
    Tests whether ``put_failed_user_ids_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Value to serialize.
    defaults : `bool`
        Whether values as their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_failed_user_ids_into(input_value, {}, defaults)
