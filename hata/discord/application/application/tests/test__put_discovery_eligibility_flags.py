import vampytest

from ..fields import put_discovery_eligibility_flags
from ..flags import ApplicationDiscoveryEligibilityFlags


def _iter_options():
    yield ApplicationDiscoveryEligibilityFlags(0), False, {}
    yield ApplicationDiscoveryEligibilityFlags(0), True, {'discovery_eligibility_flags': 0}
    yield ApplicationDiscoveryEligibilityFlags(1), False, {'discovery_eligibility_flags': 1}
    yield ApplicationDiscoveryEligibilityFlags(1), True, {'discovery_eligibility_flags': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_discovery_eligibility_flags(input_value, defaults):
    """
    Tests whether ``put_discovery_eligibility_flags`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationDiscoveryEligibilityFlags``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_discovery_eligibility_flags(input_value, {}, defaults)
