import vampytest

from ..fields import parse_type
from ..preinstanced import ApplicationCommandOptionType


def _iter_options():
    yield {}, ApplicationCommandOptionType.none
    yield {'type': ApplicationCommandOptionType.string.value}, ApplicationCommandOptionType.string


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationCommandOptionType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, ApplicationCommandOptionType)
    return output
