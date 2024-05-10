import vampytest

from ..fields import parse_user_ids


def _iter_options():
    user_id_0 = 202212250007
    user_id_1 = 202212250008
    
    yield {}, set()
    yield {'users': None}, set()
    yield {'users': [str(user_id_0)]}, {user_id_0}
    yield {'users': [str(user_id_0), str(user_id_1)]}, {user_id_0, user_id_1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_user_ids(input_data):
    """
    Tests whether ``parse_user_ids`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        data to parse from.
    
    Returns
    -------
    output : `set<int>`
    """
    output = parse_user_ids(input_data)
    vampytest.assert_instance(output, set)
    for element in output:
        vampytest.assert_instance(element, int)
    return output
