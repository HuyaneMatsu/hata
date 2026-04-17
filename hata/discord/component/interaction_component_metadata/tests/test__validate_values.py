import vampytest

from ..fields import validate_values


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
def test__validate_values(input_value):
    """
    Validates whether ``validate_values`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<str>`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_values(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
