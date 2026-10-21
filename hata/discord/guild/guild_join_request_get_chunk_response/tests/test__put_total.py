import vampytest

from ..fields import put_total


def _iter_options():
    yield (
        0,
        False,
        {
            'total': 0,
        },
    )
    
    yield (
        0,
        True,
        {
            'total': 0,
        },
    )
    
    yield (
        1,
        False,
        {
            'total': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'total': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_total(input_value, defaults):
    return put_total(input_value, {}, defaults)
