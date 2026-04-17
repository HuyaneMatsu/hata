import vampytest

from ..fields import parse_approximate_user_count


def _iter_options():
    yield {}, 0
    yield {'approximate_member_count': None}, 0
    yield {'approximate_member_count': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_approximate_user_count(input_data):
    """
    Tests whether ``parse_approximate_user_count`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse the value from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_approximate_user_count(input_data)
    vampytest.assert_instance(output, int)
    return output
