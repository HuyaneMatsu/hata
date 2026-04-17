import vampytest

from ....core import BUILTIN_EMOJIS

from ...guild_activity_overview_tag import GuildActivityOverviewTag

from ..fields import validate_tags


def _iter_options__passing():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['mushroom']
    
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            GuildActivityOverviewTag(emoji = emoji_1, title = 'stew'),
            GuildActivityOverviewTag(emoji = emoji_0, title = 'soup'),
        ],
        (
            GuildActivityOverviewTag(emoji = emoji_1, title = 'stew'),
            GuildActivityOverviewTag(emoji = emoji_0, title = 'soup'),
        ),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_tags(tags):
    """
    Tests whether ``validate_tags`` works as intended.
    
    Parameters
    ----------
    tags : `object`
        Activities to validate.
    
    Returns
    -------
    output : `None | tuple<GuildActivityOverviewTag>`
    
    Raises
    ------
    TypeError
        - If `tags` type is incorrect.
    """
    return validate_tags(tags)
