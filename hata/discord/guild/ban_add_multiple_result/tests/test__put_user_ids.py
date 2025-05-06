import vampytest

from ..fields import put_user_ids


def _iter_options():
    user_id_0 = 202405010076
    
    yield set(), False, {'user_ids': []}
    yield set(), True, {'user_ids': []}
    yield {user_id_0}, False, {'user_ids': [str(user_id_0)]}
    yield {user_id_0}, True, {'user_ids': [str(user_id_0)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user_ids(input_value, defaults):
    """
    Tests whether ``put_user_ids`` is working as intended.
    
    Parameters
    ----------
    input_value : `set<int>`
        Value to serialize.
    defaults : `bool`
        Whether values as their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_user_ids(input_value, {}, defaults)
