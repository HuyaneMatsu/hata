import vampytest

from ..fields import put_type_into
from ..preinstanced import ChannelType


def _iter_options():
    yield ChannelType.guild_text, False, {'type': ChannelType.guild_text.value}
    yield ChannelType.guild_text, True, {'type': ChannelType.guild_text.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type_into(input_value, defaults):
    """
    Tests whether ``put_type_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ChannelType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type_into(input_value, {}, defaults)
