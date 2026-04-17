import vampytest

from ....guild import GuildActivityOverview, NsfwLevel

from ..fields import put_guild_activity_overview


def _iter_options():
    yield None, False, {}
    yield None, True, {'profile': None}
    
    guild_id = 202504270001
    name = 'Remilia'
    
    guild_activity_overview = GuildActivityOverview.precreate(
        guild_id,
        name = name,
    )
    
    expected_output = {
        'profile': {
            'description': '',
            'name': 'Remilia',
            'visibility': 2,
            'traits': [],
            'game_activity': {},
            'online_count': 0,
            'member_count': 0,
            'badge': 0,
            'badge_color_primary': None,
            'badge_color_secondary': None,
            'tag': '',
            'premium_tier': 0,
            'features': [],
            'id': str(guild_id),
        },
    }
    yield guild_activity_overview, False, expected_output
    
    expected_output = {
        'profile': {
            'game_application_ids': [],
            'brand_color_primary': None,
            'description': '',
            'custom_banner_hash': None,
            'icon': None,
            'name': 'Remilia',
            'visibility': 2,
            'traits': [],
            'game_activity': {},
            'online_count': 0,
            'member_count': 0,
            'badge': 0,
            'badge_color_primary': None,
            'badge_color_secondary': None,
            'badge_hash': None,
            'tag': '',
            'premium_subscription_count': 0,
            'premium_tier': 0,
            'features': [],
            'id': str(guild_id),
        },
    }
    yield guild_activity_overview, True, expected_output


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild_activity_overview(guild_activity_overview, defaults):
    """
    Tests whether ``put_guild_activity_overview`` works as intended.
    
    Parameters
    ----------
    guild_activity_overview : ``None | GuildActivityOverview``
        The guild activity overview to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_guild_activity_overview(guild_activity_overview, {}, defaults)
