import vampytest

from ....core import BUILTIN_EMOJIS

from ...guild_activity_overview_tag import GuildActivityOverviewTag

from ..fields import put_tags


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['mushroom']
    
    yield (
        None,
        False,
        {
            'traits': [],
        },
    )
    
    yield (
        None,
        True,
        {
            'traits': [],
        },
    )
    
    yield (
        (
            GuildActivityOverviewTag(emoji = emoji_1, title = 'stew'),
            GuildActivityOverviewTag(emoji = emoji_0, title = 'soup'),
        ),
        False,
        {
            'traits': [
                {
                    'emoji_name': emoji_1.unicode,
                    'position': 0,
                    'label': 'stew',
                }, {
                    'emoji_name': emoji_0.unicode,
                    'position': 1,
                    'label': 'soup',
                }
            ]
        },
    )
    
    yield (
        (
            GuildActivityOverviewTag(emoji = emoji_1, title = 'stew'),
            GuildActivityOverviewTag(emoji = emoji_0, title = 'soup'),
        ),
        True,
        {
            'traits': [
                {
                    'emoji_name': emoji_1.unicode,
                    'position': 0,
                    'label': 'stew',
                }, {
                    'emoji_name': emoji_0.unicode,
                    'position': 1,
                    'label': 'soup',
                }
            ]
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_tags(tags, defaults):
    """
    Tests whether ``put_tags`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to put from.
    
    tags : `None | tuple<GuildActivityOverviewTag>`
        Tags to serialize.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `None | dict<int, object>`
    """
    return put_tags(tags, {}, defaults)
