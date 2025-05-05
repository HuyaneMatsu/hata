import vampytest

from ..fields import parse_required


def _iter_options():
    yield {}, True
    yield {'required': None}, True
    yield {'required': False}, False
    yield {'required': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_required(input_data):
    """
    Tests whether ``parse_required`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_required(input_data)
    vampytest.assert_instance(output, bool)
    return output
