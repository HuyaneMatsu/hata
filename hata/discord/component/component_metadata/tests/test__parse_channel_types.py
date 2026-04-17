import vampytest

from ....channel import ChannelType

from ..fields import parse_channel_types


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'channel_types': None,
        },
        None,
    )
    
    yield (
        {
            'channel_types': [],
        },
        None,
    )
    
    yield (
        {
            'channel_types': [ChannelType.private.value],
        },
        (ChannelType.private.value,),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_channel_types(input_data):
    """
    Tests whether ``parse_channel_types`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<ChannelType>``
    """
    output = parse_channel_types(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
