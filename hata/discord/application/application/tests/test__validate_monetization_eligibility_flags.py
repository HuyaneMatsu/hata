import vampytest

from ..fields import validate_monetization_eligibility_flags
from ..flags import ApplicationMonetizationEligibilityFlags


def iter_options__passing():
    yield None, ApplicationMonetizationEligibilityFlags(0)
    yield 1, ApplicationMonetizationEligibilityFlags(1)
    yield ApplicationMonetizationEligibilityFlags(1), ApplicationMonetizationEligibilityFlags(1)


def iter_options__type_error():
    yield 'a'
    yield 12.6


@vampytest._(vampytest.call_from(iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(iter_options__type_error()).raising(TypeError))
def test__validate_monetization_eligibility_flags(input_value):
    """
    Tests whether `validate_monetization_eligibility_flags` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The object to validate.
    
    Returns
    -------
    value : ``ApplicationMonetizationEligibilityFlags``
        The validated value.
    
    Raises
    ------
    TypeError
    """
    output = validate_monetization_eligibility_flags(input_value)
    vampytest.assert_instance(output, ApplicationMonetizationEligibilityFlags)
    return output
