import vampytest

from ..fields import parse_monetization_eligibility_flags
from ..flags import ApplicationMonetizationEligibilityFlags


def _iter_options():
    yield {}, ApplicationMonetizationEligibilityFlags(0)
    yield {'monetization_eligibility_flags': 1}, ApplicationMonetizationEligibilityFlags(1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_monetization_eligibility_flags(input_data):
    """
    Tests whether ``parse_monetization_eligibility_flags`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the monetization_eligibility_flags from.
    
    Returns
    -------
    output : ``ApplicationMonetizationEligibilityFlags``
    """
    output = parse_monetization_eligibility_flags(input_data)
    vampytest.assert_instance(output, ApplicationMonetizationEligibilityFlags)
    return output
