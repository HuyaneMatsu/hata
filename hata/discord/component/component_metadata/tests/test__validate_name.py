import vampytest

from ..fields import validate_name


def _iter_options__passing():
    yield None, ''
    yield '', ''
    yield 'elly', 'elly'


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_name(input_value):
    """
    Tests whether ``validate_name`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The validate.
    
    Returns
    -------
    output : `None | str`
    
    Raises
    ------
    TypeError
    """
    output = validate_name(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
