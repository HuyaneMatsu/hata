import vampytest

from ..fields import parse_channel_ids


def _iter_options():
    channel_id_0 = 202303030005
    channel_id_1 = 202303030006
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'channel_ids': None,
        },
        None,
    )
    
    yield (
        {
            'channel_ids': [],
        },
        None,
    )
    
    yield (
        {
            'channel_ids': [
                str(channel_id_0),
                str(channel_id_1),
            ],
        },
        (
            channel_id_0,
            channel_id_1,
        ),
    )
    
    yield (
        {
            'channel_ids': [
                str(channel_id_1),
                str(channel_id_0),
            ],
        },
        (
            channel_id_0,
            channel_id_1,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_channel_ids(input_data):
    """
    Tests whether ``parse_channel_ids`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = parse_channel_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, int)
    
    return output
