import vampytest

from ..fields import parse_id


def _iter_options():
    guild_boost_id = 202507060006
    
    yield (
        {},
        0,
    )
    
    yield (
        {
            'id': None,
        },
        0,
    )
    
    yield (
        {
            'id': str(guild_boost_id),
        },
        guild_boost_id,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_id(input_data):
    """
    Tests whether ``parse_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_id(input_data)
    vampytest.assert_instance(output, int)
    return output
