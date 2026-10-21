import vampytest

from ...guild_badge import GuildBadge

from ..fields import parse_badge


def _iter_options():
    guild_badge = GuildBadge(guild_id = 202610090000, tag = 'meow')
    
    yield (
        {},
        (False, None),
    )
    
    yield (
        {
            'profile': None,
        },
        (True, None),
    )
    
    yield (
        {
            'profile': guild_badge.to_data(),
        },
        (True, guild_badge),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_badge(data):
    hit, badge = parse_badge(data)
    vampytest.assert_instance(hit, bool)
    vampytest.assert_instance(badge, GuildBadge, nullable = True)
    return hit, badge
