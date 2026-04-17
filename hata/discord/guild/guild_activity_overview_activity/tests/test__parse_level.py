import vampytest

from ..fields import parse_level
from ..preinstanced import GuildActivityOverviewActivityLevel


def _iter_options():
    yield (
        {},
        GuildActivityOverviewActivityLevel.none,
    )
    
    yield (
        {'activity_level': None},
        GuildActivityOverviewActivityLevel.none,
    )
    
    yield (
        {'activity_level': GuildActivityOverviewActivityLevel.any_previous.value},
        GuildActivityOverviewActivityLevel.any_previous,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_level(input_data):
    """
    Tests whether ``parse_level`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``GuildActivityOverviewActivityLevel``
    """
    output = parse_level(input_data)
    vampytest.assert_instance(output, GuildActivityOverviewActivityLevel)
    return output
