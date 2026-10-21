import vampytest

from ..fields_common import put_description__optional


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
            'description': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'description': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'description': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_description__optional(input_value, defaults):
    return put_description__optional(input_value, {}, defaults)
