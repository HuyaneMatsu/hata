import vampytest

from ....scheduled_event import PrivacyLevel

from ..fields import validate_privacy_level


def _iter_options__passing():
    yield None, PrivacyLevel.none
    yield PrivacyLevel.public, PrivacyLevel.public
    yield PrivacyLevel.public.value, PrivacyLevel.public


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_privacy_level(input_value):
    """
    Tests whether `validate_privacy_level` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``PrivacyLevel``
    
    Raises
    ------
    TypeError
    """
    output = validate_privacy_level(input_value)
    vampytest.assert_instance(output, PrivacyLevel)
    return output
