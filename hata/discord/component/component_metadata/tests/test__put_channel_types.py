import vampytest

from ....channel import ChannelType

from ..fields import put_channel_types


def _iter_options():
    yield (
        None,
        False,
        {
            'channel_types': [],
        },
    )
    
    yield (
        None,
        True,
        {
            'channel_types': [],
        },
    )
    
    yield (
        (ChannelType.private,),
        False,
        {
            'channel_types': [ChannelType.private.value],
        },
    )
    
    yield (
        (ChannelType.private,),
        True,
        {
            'channel_types': [ChannelType.private.value],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_channel_types(input_value, defaults):
    """
    Tests whether ``put_channel_types`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<ChannelType>``
        The value to serialize.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_channel_types(input_value, {}, defaults)
