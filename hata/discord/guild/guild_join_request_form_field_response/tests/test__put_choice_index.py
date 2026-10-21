import vampytest

from ..fields import put_choice_index


def _iter_options():
    yield (
        -1,
        False,
        {},
    )
    
    yield (
        -1,
        True,
        {
            'response': -1,
        },
    )
    
    yield (
        1,
        False,
        {
            'response': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'response': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_choice_index(input_value, defaults):
    return put_choice_index(input_value, {}, defaults)
