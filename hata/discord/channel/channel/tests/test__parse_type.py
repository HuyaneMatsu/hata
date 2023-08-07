import vampytest

from ..fields import parse_type
from ..preinstanced import ChannelType


def _iter_options():
    yield {}, ChannelType.unknown
    yield {'type': ChannelType.guild_text.value}, ChannelType.guild_text


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
    output : ``ChannelType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, ChannelType)
    return output
