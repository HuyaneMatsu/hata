import vampytest

from ....guild import Guild, NsfwLevel

from ..fields import put_guild


def _iter_options():
    yield None, False, {'guild': None, 'guild_id': None}
    yield None, True, {'guild': None, 'guild_id': None}
    
    guild_id = 202307290012
    name = 'Remilia'
    
    guild = Guild.precreate(
        guild_id,
        name = name,
    )
    
    expected_output = {
        'guild': {
            'id': str(guild_id),
            'name': name,
            'unavailable': False,
            'description': '',
            'discovery_splash': None,
            'features': [],
            'icon': None,
            'splash': None,
            'nsfw_level': NsfwLevel.none,
            'verification_level': 0,
        },
        'guild_id': str(guild_id),
    }
    yield guild, False, expected_output
    
    expected_output = {
        'guild': {
            'id': str(guild_id),
            'name': name,
            'unavailable': False,
            'description': '',
            'discovery_splash': None,
            'features': [],
            'icon': None,
            'splash': None,
            'nsfw_level': NsfwLevel.none,
            'verification_level': 0,
        },
        'guild_id': str(guild_id),
    }
    
    yield guild, True, expected_output


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild(guild, defaults):
    """
    Tests whether ``put_guild`` works as intended.
    
    Parameters
    ----------
    guild : ``None | Guild``
        The guild to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_guild(guild, {}, defaults)
