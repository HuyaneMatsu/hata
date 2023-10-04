import vampytest

from ..fields import parse_deleted


def _iter_options():
    yield {}, False
    yield {'deleted': False}, False
    yield {'deleted': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_deleted(input_data):
    """
    Tests whether ``parse_deleted`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_deleted(input_data)
