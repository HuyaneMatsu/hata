import vampytest

from ...embed_field_base import EmbedMediaFlag

from ..fields import validate_flags


def _iter_options__passing():
    yield None, EmbedMediaFlag(0)
    yield 1, EmbedMediaFlag(1)
    yield EmbedMediaFlag(1), EmbedMediaFlag(1)


def _iter_options__type_error():
    yield 'a'
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_flags(input_value):
    """
    Tests whether `validate_flags` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    value : ``EmbedMediaFlag``
    
    Raises
    ------
    TypeError
    """
    output = validate_flags(input_value)
    vampytest.assert_instance(output, EmbedMediaFlag)
    return output
