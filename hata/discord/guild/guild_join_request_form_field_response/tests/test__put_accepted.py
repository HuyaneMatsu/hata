import vampytest

from ..fields import put_accepted


def _iter_options():
    yield (
        False,
        False,
        {
            'response': False,
        },
    )
    
    yield (
        False,
        True,
        {
            'response': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'response': True,
        },
    )
    
    yield (
        True,
        True,
        {
            'response': True,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_accepted(input_value, defaults):
    return put_accepted(input_value, {}, defaults)
