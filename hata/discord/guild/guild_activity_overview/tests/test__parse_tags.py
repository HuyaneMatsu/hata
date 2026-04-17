import vampytest

from ....core import BUILTIN_EMOJIS

from ...guild_activity_overview_tag import GuildActivityOverviewTag

from ..fields import parse_tags


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['mushroom']
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'traits': None,
        },
        None,
    )
    
    yield (
        {
            'traits': [],
        },
        None,
    )
    
    yield (
        {
            'traits': [
                {
                    'emoji_name': emoji_0.unicode,
                    'position': 2,
                    'label': 'soup',
                }, {
                    'emoji_name': emoji_1.unicode,
                    'position': 1,
                    'label': 'stew',
                }
            ]
        },
        (
            GuildActivityOverviewTag(emoji = emoji_1, title = 'stew'),
            GuildActivityOverviewTag(emoji = emoji_0, title = 'soup'),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_tags(input_data):
    """
    Tests whether ``parse_tags`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<GuildActivityOverviewTag>`
    """
    output = parse_tags(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
