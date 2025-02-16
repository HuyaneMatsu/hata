import vampytest

from ..fields import put_mentioned_role_ids


def _iter_options():
    role_id = 202305010016
    
    yield None, False, {}
    yield None, True, {'mention_roles': []}
    yield (role_id, ), False, {'mention_roles': [str(role_id)]}
    yield (role_id, ), True, {'mention_roles': [str(role_id)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mentioned_role_ids(input_value, defaults):
    """
    Tests whether ``put_mentioned_role_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Value to serialize.
    defaults : `bool`
        Whether values as their default should be serialized as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_mentioned_role_ids(input_value, {}, defaults)
