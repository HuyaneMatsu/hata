import vampytest

from ....scheduled_event import PrivacyLevel

from ..fields import put_privacy_level


def _iter_options():
    yield PrivacyLevel.none, False, {'privacy_level': PrivacyLevel.public.none}
    yield PrivacyLevel.none, True, {'privacy_level': PrivacyLevel.public.none}
    yield PrivacyLevel.public, False, {'privacy_level': PrivacyLevel.public.value}
    yield PrivacyLevel.public, True, {'privacy_level': PrivacyLevel.public.value}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_privacy_level(input_value, defaults):
    """
    Tests whether ``put_privacy_level`` works as intended.
    
    Parameters
    ----------
    input_value : ``PrivacyLevel``
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_privacy_level(input_value, {}, defaults)
