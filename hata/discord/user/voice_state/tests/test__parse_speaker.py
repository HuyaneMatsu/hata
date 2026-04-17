import vampytest

from ..fields import parse_speaker


def _iter_options():
    yield {}, False
    yield {'suppress': None}, False
    yield {'suppress': True}, False
    yield {'suppress': False}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_speaker(input_data):
    """
    Tests whether ``parse_speaker`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_speaker(input_data)
