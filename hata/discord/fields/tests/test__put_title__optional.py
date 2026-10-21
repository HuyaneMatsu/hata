import vampytest

from ..fields_common import put_title__optional


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
            'title': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'title': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'title': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_title__optional(input_value, defaults):
    return put_title__optional(input_value, {}, defaults)
