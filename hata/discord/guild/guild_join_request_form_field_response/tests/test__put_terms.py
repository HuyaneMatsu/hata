import vampytest

from ..fields import put_terms


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
            'values': [],
        }
    )
    
    yield (
        (
            'apple',
            'pear',
        ),
        False,
        {
            'values': [
                'apple',
                'pear',
            ],
        },
    )
    
    yield (
        (
            'apple',
            'pear',
        ),
        True,
        {
            'values': [
                'apple',
                'pear',
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_terms(input_value, defaults):
    return put_terms(input_value, {}, defaults)
