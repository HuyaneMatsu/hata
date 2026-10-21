import vampytest

from ..fields import validate_terms


def _iter_options__passing():
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            'apple',
            'pear',
        ],
        (
            'apple',
            'pear',
        ),
    )
    
    yield (
        [
            'pear',
            'apple',
        ],
        (
            'apple',
            'pear',
        ),
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_terms(input_value):
    output = validate_terms(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
