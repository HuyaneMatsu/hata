import vampytest

from ..fields_common import parse_user_id


def _iter_options():
    user_id = 202305160008
    
    yield (
        {},
        0,
    )
    
    yield (
        {
            'user_id': None,
        },
        0,
    )
    
    yield (
        {
            'user_id': str(user_id),
        },
        user_id,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_user_id(input_data):
    output = parse_user_id(input_data)
    vampytest.assert_instance(output, int)
    return output
