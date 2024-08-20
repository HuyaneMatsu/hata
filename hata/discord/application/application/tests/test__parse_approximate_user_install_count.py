import vampytest

from ..fields import parse_approximate_user_install_count


def _iter_options():
    yield {}, 0
    yield {'approximate_user_install_count': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_approximate_user_install_count(input_data):
    """
    Tests whether ``parse_approximate_user_install_count`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse the value from.
    
    Returns
    -------
    output : `int`
    """
    return parse_approximate_user_install_count(input_data)
