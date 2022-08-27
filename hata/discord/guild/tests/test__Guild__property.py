import vampytest

from .. import Guild, NsfwLevel


def test__ConnectionType__nsfw_0():
    """
    Tests whether `Guild.nsfw` returns the correct value.
    
    Case: NsfwLevel.safe
    """
    nsfw_level = NsfwLevel.safe
    guild = Guild.precreate(202208270000, nsfw_level=nsfw_level)
    
    vampytest.assert_eq(guild.nsfw, nsfw_level.nsfw)


def test__ConnectionType__nsfw_1():
    """
    Tests whether `Guild.nsfw` returns the correct value.
    
    Case: NsfwLevel.explicit
    """
    nsfw_level = NsfwLevel.explicit
    guild = Guild.precreate(202208270000, nsfw_level=nsfw_level)
    
    vampytest.assert_eq(guild.nsfw, nsfw_level.nsfw)
