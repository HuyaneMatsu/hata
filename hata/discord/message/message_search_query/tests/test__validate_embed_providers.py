import vampytest

from ..fields import validate_embed_providers


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
            'fry',
            'shrimp',
        ],
        (
            'fry',
            'shrimp',
        ),
    )
    
    yield (
        [
            'shrimp',
            'fry',
        ],
        (
            'fry',
            'shrimp',
        ),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_embed_providers(input_value):
    """
    Tests whether `validate_embed_providers` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `None | tuple<str>`
    
    Raises
    ------
    TypeError
    """
    output = validate_embed_providers(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
