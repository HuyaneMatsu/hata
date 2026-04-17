import vampytest

from ..shared_constants import LABEL_LENGTH_MAX
from ..shared_fields import validate_label


def _iter_options__passing():
    yield None, ''
    yield 'a', 'a'


def _iter_options__type_error():
    yield 12.6


def _iter_options__label_error():
    yield 'a' * (LABEL_LENGTH_MAX + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__label_error()).raising(ValueError))
def test__validate_label(input_label):
    """
    Validates whether ``validate_label`` works as intended.
    
    Parameters
    ----------
    input_label : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_label(input_label)
    vampytest.assert_instance(output, str, nullable = True)
    return output
