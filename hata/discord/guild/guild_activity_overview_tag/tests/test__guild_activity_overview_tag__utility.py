import vampytest

from ....core import BUILTIN_EMOJIS

from ..guild_activity_overview_tag import GuildActivityOverviewTag

from .test__guild_activity_overview_tag__constructor import _assert_fields_set


def test__GuildActivityOverviewTag__copy():
    """
    Tests whether ``GuildActivityOverviewTag.copy`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    title = 'soup'
    
    guild_activity_overview_tag = GuildActivityOverviewTag(emoji = emoji, title = title)
    
    copy = guild_activity_overview_tag.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_activity_overview_tag)
    
    vampytest.assert_eq(copy.emoji, emoji)
    vampytest.assert_eq(copy.title, title)


def test__GuildActivityOverviewTag__copy_with__no_fields():
    """
    Tests whether ``GuildActivityOverviewTag.copy`` works as intended.
    
    Case: no fields given.
    """
    emoji = BUILTIN_EMOJIS['heart']
    title = 'soup'
    
    guild_activity_overview_tag = GuildActivityOverviewTag(emoji = emoji, title = title)
    
    copy = guild_activity_overview_tag.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_activity_overview_tag)
    
    vampytest.assert_eq(copy.emoji, emoji)
    vampytest.assert_eq(copy.title, title)


def test__GuildActivityOverviewTag__copy_with__all_fields():
    """
    Tests whether ``GuildActivityOverviewTag.copy`` works as intended.
    
    Case: all fields given.
    """
    old_emoji = BUILTIN_EMOJIS['heart']
    old_title = 'soup'
    
    new_emoji = BUILTIN_EMOJIS['mushroom']
    new_title = 'stew'
    
    guild_activity_overview_tag = GuildActivityOverviewTag(emoji = old_emoji, title = old_title)
    
    copy = guild_activity_overview_tag.copy_with(emoji = new_emoji, title = new_title)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_activity_overview_tag)
    
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.title, new_title)
