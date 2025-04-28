import vampytest

from ..fields import put_level
from ..preinstanced import GuildActivityOverviewActivityLevel


def _iter_options():
    yield (
        GuildActivityOverviewActivityLevel.none,
        False,
        {'activity_level': GuildActivityOverviewActivityLevel.none.value},
    )
    
    yield (
        GuildActivityOverviewActivityLevel.none,
        True,
        {'activity_level': GuildActivityOverviewActivityLevel.none.value},
    )
    
    yield (
        GuildActivityOverviewActivityLevel.any_previous,
        False,
        {'activity_level': GuildActivityOverviewActivityLevel.any_previous.value},
    )
    
    yield (
        GuildActivityOverviewActivityLevel.any_previous,
        True,
        {'activity_level': GuildActivityOverviewActivityLevel.any_previous.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_level(input_value, defaults):
    """
    Tests whether ``put_level`` is working as intended.
    
    Parameters
    ----------
    input_value : ``GuildActivityOverviewActivityLevel``
        Value to serialize.
    
    defaults : `bool`
        Whether values as their default should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_level(input_value, {}, defaults)
