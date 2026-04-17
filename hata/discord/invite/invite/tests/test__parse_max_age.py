import vampytest

from ..fields import parse_max_age


def _iter_options():
    yield {}, None
    yield {'max_age': None}, None
    yield {'max_age': 0}, 0
    yield {'max_age': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_max_age(input_data):
    """
    Tests whether ``parse_max_age`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse from.
    
    Returns
    -------
    output : `None | int`
    """
    return parse_max_age(input_data)
