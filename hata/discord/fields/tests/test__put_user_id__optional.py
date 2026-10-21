import vampytest

from ..fields_common import put_user_id__optional


def _iter_options():
    user_id = 202610110001
    
    yield (
        0,
        False,
        {},
    )
    
    yield (
        0,
        True,
        {
            'user_id': None,
        },
    )
    
    yield (
        user_id,
        False,
        {
            'user_id': str(user_id),
        },
    )
    
    yield (
        user_id,
        True,
        {
            'user_id': str(user_id),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user_id__optional(input_value, defaults):
    return put_user_id__optional(input_value, {}, defaults)
