import vampytest

from ..fields import parse_discovery_eligibility_flags
from ..flags import ApplicationDiscoveryEligibilityFlags


def _iter_options():
    yield {}, ApplicationDiscoveryEligibilityFlags(0)
    yield {'discovery_eligibility_flags': 1}, ApplicationDiscoveryEligibilityFlags(1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_discovery_eligibility_flags(input_data):
    """
    Tests whether ``parse_discovery_eligibility_flags`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the discovery_eligibility_flags from.
    
    Returns
    -------
    output : ``ApplicationDiscoveryEligibilityFlags``
    """
    output = parse_discovery_eligibility_flags(input_data)
    vampytest.assert_instance(output, ApplicationDiscoveryEligibilityFlags)
    return output
