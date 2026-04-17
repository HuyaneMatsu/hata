import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..guild_activity_overview_tag import GuildActivityOverviewTag


def _assert_fields_set(guild_activity_overview_tag):
    """
    Asserts whether the given guild activity overview tag has all of its fields set.
    
    Parameters
    ----------
    guild_activity_overview_tag : ``GuildActivityOverviewTag``
        Guild activity overview to test.
    """
    vampytest.assert_instance(guild_activity_overview_tag, GuildActivityOverviewTag)
    vampytest.assert_instance(guild_activity_overview_tag.emoji, Emoji, nullable = True)
    vampytest.assert_instance(guild_activity_overview_tag.title, str)



def test__GuildActivityOverviewTag__new__no_fields():
    """
    Tests whether ``GuildActivityOverviewTag.__new__`` works as intended.
    
    Case: no fields given.
    """
    guild_activity_overview_tag = GuildActivityOverviewTag()
    _assert_fields_set(guild_activity_overview_tag)


def test__GuildActivityOverviewTag__new__all_fields():
    """
    Tests whether ``GuildActivityOverviewTag.__new__`` works as intended.
    
    Case: all fields given.
    """
    emoji = BUILTIN_EMOJIS['heart']
    title = 'soup'
    
    guild_activity_overview_tag = GuildActivityOverviewTag(emoji = emoji, title = title)
    _assert_fields_set(guild_activity_overview_tag)
    
    vampytest.assert_is(guild_activity_overview_tag.emoji, emoji)
    vampytest.assert_eq(guild_activity_overview_tag.title, title)
