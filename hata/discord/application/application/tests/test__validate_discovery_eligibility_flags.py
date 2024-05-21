import vampytest

from ..fields import validate_discovery_eligibility_flags
from ..flags import ApplicationDiscoveryEligibilityFlags


def _iter_options__passing():
    yield None, ApplicationDiscoveryEligibilityFlags(0)
    yield 1, ApplicationDiscoveryEligibilityFlags(1)
    yield ApplicationDiscoveryEligibilityFlags(1), ApplicationDiscoveryEligibilityFlags(1)


def _iter_options__type_error():
    yield 'a'
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_discovery_eligibility_flags(input_value):
    """
    Tests whether `validate_discovery_eligibility_flags` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The object to validate.
    
    Returns
    -------
    value : ``ApplicationDiscoveryEligibilityFlags``
        The validated value.
    
    Raises
    ------
    TypeError
    """
    output = validate_discovery_eligibility_flags(input_value)
    vampytest.assert_instance(output, ApplicationDiscoveryEligibilityFlags)
    return output
