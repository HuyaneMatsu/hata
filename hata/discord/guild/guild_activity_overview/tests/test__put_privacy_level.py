import vampytest

from ....scheduled_event import PrivacyLevel

from ..fields import put_privacy_level


def _iter_options():
    yield (
        PrivacyLevel.guild_only,
        False,
        {
            'visibility': PrivacyLevel.guild_only.value,
        },
    )
    
    yield (
        PrivacyLevel.guild_only,
        True,
        {
            'visibility': PrivacyLevel.guild_only.value,
        },
    )
    
    yield (
        PrivacyLevel.public,
        False,
        {
            'visibility': PrivacyLevel.public.value,
        },
    )
    
    yield (
        PrivacyLevel.public,
        True,
        {
            'visibility': PrivacyLevel.public.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_privacy_level(input_value, defaults):
    """
    Tests whether ``put_privacy_level`` is working as intended.
    
    Parameters
    ----------
    input_value : ``PrivacyLevel``
        The value to serialize.
    
    defaults : `bool`
        Whether values with their default should be serialized as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_privacy_level(input_value, {}, defaults)
