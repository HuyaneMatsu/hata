import vampytest

from ..fields import validate_status
from ..preinstanced import SubscriptionStatus


def _iter_options__passing():
    yield None, SubscriptionStatus.active
    yield SubscriptionStatus.ending, SubscriptionStatus.ending
    yield SubscriptionStatus.ending.value, SubscriptionStatus.ending


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_status(input_value):
    """
    Validates whether ``validate_status`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``SubscriptionStatus``
    
    Raises
    ------
    TypeError
    """
    output = validate_status(input_value)
    vampytest.assert_instance(output, SubscriptionStatus)
    return output
