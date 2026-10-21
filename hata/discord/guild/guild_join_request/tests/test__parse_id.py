import vampytest

from ..fields import parse_id


def _iter_options():
    guild_join_request_id = 202610100000
    
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
            'id': str(guild_join_request_id),
        },
        guild_join_request_id,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_id(input_data):
    output = parse_id(input_data)
    vampytest.assert_instance(output, int)
    return output
