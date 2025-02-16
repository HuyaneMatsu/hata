import vampytest

from ..fields import put_banned_user_ids


def _iter_options():
    user_id_0 = 202405010016
    user_id_1 = 202405010017
    
    yield None, False, {'banned_users': []}
    yield None, True, {'banned_users': []}
    yield (user_id_0, user_id_1,), False, {'banned_users': [str(user_id_0), str(user_id_1)]}
    yield (user_id_0, user_id_1,), True, {'banned_users': [str(user_id_0), str(user_id_1)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_banned_user_ids(input_value, defaults):
    """
    Tests whether ``put_banned_user_ids`` is working as intended.
    
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
    return put_banned_user_ids(input_value, {}, defaults)
