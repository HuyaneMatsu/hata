import vampytest

from ..fields import parse_cancelled


def _iter_options():
    yield {}, False
    yield {'is_canceled': None}, False
    yield {'is_canceled': False}, False
    yield {'is_canceled': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_cancelled(input_data):
    """
    Tests whether ``parse_cancelled`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_cancelled(input_data)
    vampytest.assert_instance(output, bool)
    return output
