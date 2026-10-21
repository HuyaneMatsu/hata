import vampytest

from ..fields import put_value


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
            'response': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'response': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'response': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_value(input_value, defaults):
    return put_value(input_value, {}, defaults)
