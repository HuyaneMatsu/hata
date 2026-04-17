import vampytest

from ..guild import Guild
from ..utils import create_partial_guild_from_id


def test__create_partial_guild_from_id__new():
    """
    Tests whether ``create_partial_guild_from_id`` works as intended.
    
    Case: New guild.
    """
    guild_id = 202307300003
    
    guild = create_partial_guild_from_id(guild_id)
    
    vampytest.assert_instance(guild, Guild)
    
    vampytest.assert_eq(guild.id, guild_id)


def test__create_partial_guild_from_id__existing():
    """
    Tests whether ``create_partial_guild_from_id`` works as intended.
    
    Case: existing guild.
    """
    guild_id = 202307300004
    
    existing_guild = Guild.precreate(guild_id)
    
    guild = create_partial_guild_from_id(guild_id)
    
    vampytest.assert_instance(guild, Guild)
    vampytest.assert_is(guild, existing_guild)


def test__create_partial_guild_from_id__caching():
    
    """
    Tests whether ``create_partial_guild_from_id`` works as intended.
    
    Case: existing guild.
    """
    guild_id = 202307300005
    
    guild_0 = create_partial_guild_from_id(guild_id)
    guild_1 = create_partial_guild_from_id(guild_id)
    
    vampytest.assert_is(guild_0, guild_1)
