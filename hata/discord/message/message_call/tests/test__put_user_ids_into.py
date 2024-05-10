import vampytest

from ..fields import put_user_ids_into


def _iter_options():
    user_id_0 = 202304270007
    user_id_1 = 202304270004
    
    yield None, False, {'participants': []}
    yield None, True, {'participants': []}
    yield (user_id_0, user_id_1,), False, {'participants': [str(user_id_0), str(user_id_1)]}
    yield (user_id_0, user_id_1,), True, {'participants': [str(user_id_0), str(user_id_1)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user_ids_into(input_value, defaults):
    """
    Tests whether ``put_user_ids_into`` is working as intended.
    
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
    return put_user_ids_into(input_value, {}, defaults)
