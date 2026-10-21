import vampytest

from ..fields import parse_choices


def _iter_options():
    yield (
        {},
        None,
    )
    
    
    yield (
        {
            'choices': None,
        },
        None,
    )
    
    yield (
        {
            'choices': [],
        },
        None,
    )
    
    yield (
        {
            'choices': [
                'apple',
                'pear',
            ],
        },
        (
            'apple',
            'pear',
        ),
    )
    
    yield (
        {
            'choices': [
                'pear',
                'apple',
            ],
        },
        (
            'apple',
            'pear',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_choices(input_data):
    output = parse_choices(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
