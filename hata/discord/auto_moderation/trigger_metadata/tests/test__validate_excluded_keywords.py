import vampytest

from ..fields import validate_excluded_keywords


def _iter_options__passing():
    yield None, None
    yield [], None
    yield 'apple', ('apple',)
    yield ['apple'], ('apple', )
    yield ['apple', 'bad'], ('apple', 'bad')
    yield ['bad', 'apple'], ('apple', 'bad')


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_excluded_keywords(input_value):
    """
    Tests whether `validate_excluded_keywords` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<str>`
        Validated value.
    
    Raises
    ------
    TypeError
    """
    output = validate_excluded_keywords(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
