import vampytest

from ......discord.component.shared_constants import CUSTOM_ID_LENGTH_MAX

from ..helpers import _validate_string_custom_id


def _iter_options__passing():
    yield 'a', 'a'
    yield 'a' * CUSTOM_ID_LENGTH_MAX, 'a' * CUSTOM_ID_LENGTH_MAX


def _iter_options__value_error():
    yield ''
    yield 'a' * (CUSTOM_ID_LENGTH_MAX + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_string_custom_id(input_value):
    """
    Tests whether ``_validate_string_custom_id`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to validate.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    ValueError
    """
    output = _validate_string_custom_id(input_value)
    vampytest.assert_instance(output, str, accept_subtypes = False)
    return output
