import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import put_partial_emoji_inline_data_into

from ..guild_activity_overview_tag import GuildActivityOverviewTag

from .test__guild_activity_overview_tag__constructor import _assert_fields_set


def test__GuildActivityOverviewTag__from_data():
    """
    Tests whether ``GuildActivityOverviewTag.from_data`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    title = 'soup'
    
    data = {
        **put_partial_emoji_inline_data_into(emoji, {}),
        'label': title,
    }
    
    guild_activity_overview_tag = GuildActivityOverviewTag.from_data(data)
    _assert_fields_set(guild_activity_overview_tag)
    
    vampytest.assert_is(guild_activity_overview_tag.emoji, emoji)
    vampytest.assert_eq(guild_activity_overview_tag.title, title)


def test__GuildActivityOverviewTag__to_data():
    """
    Tests whether ``GuildActivityOverviewTag.to_data`` works as intended.
    
    Case: include defaults.
    """
    emoji = BUILTIN_EMOJIS['heart']
    title = 'soup'
    
    expected_output = {
        **put_partial_emoji_inline_data_into(emoji, {}),
        'label': title,
    }
    
    guild_activity_overview_tag = GuildActivityOverviewTag(emoji = emoji, title = title)
    
    vampytest.assert_eq(
        guild_activity_overview_tag.to_data(defaults = True),
        expected_output,
    )
