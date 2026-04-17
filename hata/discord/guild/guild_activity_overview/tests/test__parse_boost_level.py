import vampytest

from ..fields import parse_boost_level


def _iter_options():
    yield {}, 0
    yield {'premium_tier': None}, 0
    yield {'premium_tier': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_boost_level(input_data):
    """
    Tests whether ``parse_boost_level`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_boost_level(input_data)
    vampytest.assert_instance(output, int)
    return output
