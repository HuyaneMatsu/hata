import vampytest

from ....localization import Locale

from ..guild import Guild
from ..preinstanced import GuildFeature
from ..utils import create_partial_guild_from_interaction_guild_data


def test__create_partial_guild_from_interaction_guild_data__new():
    """
    Tests whether ``create_partial_guild_from_interaction_guild_data`` works as intended.
    
    Case: creating new guild.
    """
    guild_id = 202310100001
    locale = Locale.dutch
    features = [GuildFeature.icon_animated]
    
    data = {
        'id': str(guild_id),
        'locale': locale,
        'features': [feature.value for feature in features],
    }
    
    guild = create_partial_guild_from_interaction_guild_data(data)
    
    vampytest.assert_instance(guild, Guild)
    
    vampytest.assert_eq(guild.id, guild_id)
    vampytest.assert_eq(guild.locale, locale)
    vampytest.assert_eq(guild.features, tuple(features))


def test__create_partial_guild_from_interaction_guild_data__existing():
    """
    Tests whether ``create_partial_guild_from_interaction_guild_data`` works as intended.
    
    Case: guild already exists.
    """
    guild_id = 202310100002
    
    existing_guild = Guild.precreate(guild_id)
    
    data = {
        'id': str(guild_id),
    }
    
    guild = create_partial_guild_from_interaction_guild_data(data)
    
    vampytest.assert_instance(guild, Guild)
    vampytest.assert_is(guild, existing_guild)


def test__create_partial_guild_from_interaction_guild_data__caching():
    """
    Tests whether ``create_partial_guild_from_interaction_guild_data`` works as intended.
    
    Case: caching.
    """
    guild_id = 202310100003
    
    data = {
        'id': str(guild_id),
    }
    
    guild_0 = create_partial_guild_from_interaction_guild_data(data)
    guild_1 = create_partial_guild_from_interaction_guild_data(data)
    
    vampytest.assert_is(guild_0, guild_1)
