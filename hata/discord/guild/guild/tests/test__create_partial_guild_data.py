import vampytest

from ....bases import Icon, IconType

from ..guild import Guild
from ..preinstanced import GuildFeature, VerificationLevel
from ..utils import create_partial_guild_data


def test__create_partial_guild_data():
    """
    Tests whether ``create_partial_guild_data`` works as intended.
    """
    guild_id = 202307300000
    
    available = True
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    features = [GuildFeature.animated_icon]
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    name = 'Komeiji'
    verification_level = VerificationLevel.medium
    

    expected_output = {
        'id': str(guild_id),
        'unavailable': not available,
        'description': description,
        'features': [feature.value for feature in features],
        'name': name,
        'verification_level': verification_level.value,
        'icon': icon.as_base_16_hash,
        'discovery_splash': discovery_splash.as_base_16_hash,
        'splash': invite_splash.as_base_16_hash,
    }
    

    guild = Guild.precreate(
        guild_id,
        available = available,
        description = description,
        discovery_splash = discovery_splash,
        features = features,
        icon = icon,
        invite_splash = invite_splash,
        name = name,
        verification_level = verification_level,
    )
    
    vampytest.assert_eq(
        create_partial_guild_data(guild),
        expected_output,
    )
