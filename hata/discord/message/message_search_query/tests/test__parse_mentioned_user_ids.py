import vampytest

from ..fields import parse_mentioned_user_ids


def _iter_options():
    user_id_0 = 202601030020
    user_id_1 = 202601030021
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'mentions': None,
        },
        None,
    )
    
    yield (
        {
            'mentions': [],
        },
        None,
    )
    
    yield (
        {
            'mentions': [
                str(user_id_0),
                str(user_id_1),
            ],
        },
        (
            user_id_0,
            user_id_1,
        ),
    )
    
    yield (
        {
            'mentions': [
                str(user_id_1),
                str(user_id_0),
            ],
        },
        (
            user_id_0,
            user_id_1,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_mentioned_user_ids(input_data):
    """
    Tests whether ``parse_mentioned_user_ids`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = parse_mentioned_user_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, int)
    
    return output
