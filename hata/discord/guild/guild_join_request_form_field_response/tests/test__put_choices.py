import vampytest

from ..fields import put_choices


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
            'choices': [],
        }
    )
    
    yield (
        (
            'apple',
            'pear',
        ),
        False,
        {
            'choices': [
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
            'choices': [
                'apple',
                'pear',
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_choices(input_value, defaults):
    return put_choices(input_value, {}, defaults)
