import vampytest

from ..fields import parse_analytics_id


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'analytics_id': None,
        },
        0,
    )
    
    yield (
        {
            'analytics_id': format(1, '0>32x'),
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_analytics_id(input_data):
    """
    Tests whether ``parse_analytics_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_analytics_id(input_data)
    vampytest.assert_instance(output, int)
    return output
