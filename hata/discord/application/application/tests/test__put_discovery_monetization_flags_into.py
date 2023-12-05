import vampytest

from ..fields import put_monetization_eligibility_flags_into
from ..flags import ApplicationMonetizationEligibilityFlags


def _iter_options():
    yield ApplicationMonetizationEligibilityFlags(0), False, {}
    yield ApplicationMonetizationEligibilityFlags(0), True, {'monetization_eligibility_flags': 0}
    yield ApplicationMonetizationEligibilityFlags(1), False, {'monetization_eligibility_flags': 1}
    yield ApplicationMonetizationEligibilityFlags(1), True, {'monetization_eligibility_flags': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_monetization_eligibility_flags_into(input_value, defaults):
    """
    Tests whether ``put_monetization_eligibility_flags_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationMonetizationEligibilityFlags``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_monetization_eligibility_flags_into(input_value, {}, defaults)
