import vampytest

from ..fields import parse_divider


def _iter_options():
    yield {}, True
    yield {'divider': None}, True
    yield {'divider': False}, False
    yield {'divider': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_divider(input_data):
    """
    Tests whether ``parse_divider`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_divider(input_data)
