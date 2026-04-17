import vampytest

from ....core import BUILTIN_EMOJIS

from ..guild_activity_overview_tag import GuildActivityOverviewTag


def test__GuildActivityOverviewTag__repr():
    """
    Tests whether ``GuildActivityOverviewTag.__repr__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    title = 'soup'
    
    guild_activity_overview_tag = GuildActivityOverviewTag(emoji = emoji, title = title)
    
    output = repr(guild_activity_overview_tag)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(guild_activity_overview_tag).__name__, output)
    vampytest.assert_in(f'emoji = {emoji!r}', output)
    vampytest.assert_in(f'title = {title!r}', output)


def test__GuildActivityOverviewTag__hash():
    """
    Tests whether ``GuildActivityOverviewTag.__repr__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    title = 'soup'
    
    guild_activity_overview_tag = GuildActivityOverviewTag(emoji = emoji, title = title)
    
    output = hash(guild_activity_overview_tag)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    emoji = BUILTIN_EMOJIS['heart']
    title = 'soup'
    
    keyword_parameters = {
        'emoji': emoji,
        'title': title,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'emoji': BUILTIN_EMOJIS['mushroom'],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'title': 'stew',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__GuildActivityOverviewTag__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``GuildActivityOverviewTag.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    guild_activity_overview_tag_0 = GuildActivityOverviewTag(**keyword_parameters_0)
    guild_activity_overview_tag_1 = GuildActivityOverviewTag(**keyword_parameters_1)
    
    output = guild_activity_overview_tag_0 == guild_activity_overview_tag_1
    vampytest.assert_instance(output, bool)
    return output
