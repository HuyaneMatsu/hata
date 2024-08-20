import vampytest

from ..fields import parse_privacy_level
from ..preinstanced import PrivacyLevel


def _iter_options():
    yield {}, PrivacyLevel.guild_only
    yield {'privacy_level': PrivacyLevel.guild_only.value}, PrivacyLevel.guild_only
    yield {'privacy_level': PrivacyLevel.public.value}, PrivacyLevel.public


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_privacy_level(input_data):
    """
    Tests whether ``parse_privacy_level`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``PrivacyLevel``
    """
    output = parse_privacy_level(input_data)
    vampytest.assert_instance(output, PrivacyLevel)
    return output
