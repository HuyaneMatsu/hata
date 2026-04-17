import vampytest

from ..fields import put_channel_ids


def _iter_options():
    channel_id_0 = 202303030100
    channel_id_1 = 202303030101
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'channel_ids': [],
        },
    )
    
    yield (
        (
            channel_id_0,
            channel_id_1,
        ),
        False,
        {
            'channel_ids': [
                str(channel_id_0),
                str(channel_id_1),
            ],
        },
    )
    
    yield (
        (
            channel_id_0,
            channel_id_1,
        ),
        True,
        {
            'channel_ids': [
                str(channel_id_0),
                str(channel_id_1),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_channel_ids(input_value, defaults):
    """
    Tests whether ``put_channel_ids`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        The value to serialise.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_channel_ids(input_value, {}, defaults)
