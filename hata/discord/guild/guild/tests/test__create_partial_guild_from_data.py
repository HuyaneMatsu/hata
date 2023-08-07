import vampytest

from ....bases import Icon, IconType

from ..guild import Guild
from ..preinstanced import GuildFeature, NsfwLevel, VerificationLevel
from ..utils import create_partial_guild_from_data


def test__create_partial_guild_from_data__new():
    """
    Tests whether ``create_partial_guild_from_data`` works as intended.
    
    Case: creating new guild.
    """
    guild_id = 202307300008
    available = True
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    features = [GuildFeature.animated_icon]
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    name = 'Komeiji'
    nsfw_level = NsfwLevel.explicit
    verification_level = VerificationLevel.medium
    
    data = {
        'id': str(guild_id),
        'unavailable': not available,
        'description': description,
        'features': [feature.value for feature in features],
        'name': name,
        'verification_level': verification_level.value,
        'icon': icon.as_base_16_hash,
        'discovery_splash': discovery_splash.as_base_16_hash,
        'splash': invite_splash.as_base_16_hash,
        'nsfw_level': nsfw_level.value,
    }
    
    guild = create_partial_guild_from_data(data)
    
    vampytest.assert_instance(guild, Guild)
    
    vampytest.assert_eq(guild.id, guild_id)
    vampytest.assert_eq(guild.available, available)
    vampytest.assert_eq(guild.description, description)
    vampytest.assert_eq(guild.discovery_splash, discovery_splash)
    vampytest.assert_eq(guild.features, tuple(features))
    vampytest.assert_eq(guild.icon, icon)
    vampytest.assert_eq(guild.invite_splash, invite_splash)
    vampytest.assert_eq(guild.name, name)
    vampytest.assert_is(guild.nsfw_level, nsfw_level)
    vampytest.assert_is(guild.verification_level, verification_level)


def test__create_partial_guild_from_data__existing():
    """
    Tests whether ``create_partial_guild_from_data`` works as intended.
    
    Case: guild already exists.
    """
    guild_id = 202307300009
    
    existing_guild = Guild.precreate(guild_id)
    
    data = {
        'id': str(guild_id),
    }
    
    guild = create_partial_guild_from_data(data)
    
    vampytest.assert_instance(guild, Guild)
    vampytest.assert_is(guild, existing_guild)


def test__create_partial_guild_from_data__caching():
    """
    Tests whether ``create_partial_guild_from_data`` works as intended.
    
    Case: caching.
    """
    guild_id = 202307300010
    
    data = {
        'id': str(guild_id),
    }
    
    guild_0 = create_partial_guild_from_data(data)
    guild_1 = create_partial_guild_from_data(data)
    
    vampytest.assert_is(guild_0, guild_1)
