import vampytest

from ..fields import parse_type
from ..preinstanced import EmbeddedActivityLocationType


def _iter_options():
    yield {}, EmbeddedActivityLocationType.none
    yield {'kind': EmbeddedActivityLocationType.guild_channel.value}, EmbeddedActivityLocationType.guild_channel


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
    output : ``EmbeddedActivityLocationType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, EmbeddedActivityLocationType)
    return output
