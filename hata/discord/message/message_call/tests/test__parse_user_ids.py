import vampytest

from ..fields import parse_user_ids


def _iter_options():
    user_id_0 = 202304270002
    user_id_1 = 202304270003
    
    yield {}, None
    yield {'participants': None}, None
    yield {'participants': [str(user_id_0)]}, (user_id_0,)
    yield {'participants': [str(user_id_0), str(user_id_1)]}, (user_id_0, user_id_1)


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
    output : `None | tuple<int>`
    """
    output = parse_user_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    if output is not None:
        for element in output:
            vampytest.assert_instance(element, int)
    return output
