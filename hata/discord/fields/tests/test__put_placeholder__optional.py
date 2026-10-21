import vampytest

from ..fields_common import put_placeholder__optional


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'placeholder': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'placeholder': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'placeholder': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_placeholder__optional(input_value, defaults):
    return put_placeholder__optional(input_value, {}, defaults)
