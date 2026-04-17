import vampytest

from ...emoji import Emoji

from ..request_helpers import get_emoji_and_guild_id_and_id


def _iter_options__passing():
    emoji_id = 202407260009
    guild_id = 202407260010
    
    yield (
        (guild_id, emoji_id),
        [],
        (None, guild_id, emoji_id),
    )
    
    emoji_id = 202407260011
    guild_id = 202407260012
    
    yield (
        (str(guild_id), str(emoji_id)),
        [],
        (None, guild_id, emoji_id),
    )
    
    emoji_id = 202407260013
    guild_id = 202407260014
    emoji = Emoji.precreate(emoji_id, guild_id = guild_id)
    
    yield (
        emoji,
        [emoji],
        (emoji, guild_id, emoji_id),
    )
    
    
    emoji_id = 202407260015
    guild_id = 0
    emoji = Emoji.precreate(emoji_id, guild_id = guild_id)
    
    yield (
        emoji,
        [emoji],
        (emoji, guild_id, emoji_id),
    )


    emoji_id = 202407260016
    guild_id = 202407260017
    emoji = Emoji.precreate(emoji_id, guild_id = guild_id)
    
    yield (
        (guild_id, emoji_id),
        [emoji],
        (emoji, guild_id, emoji_id),
    )


def _iter_options__type_error():
    yield None, []
    yield 12.6, []
    yield ((202407260018, 'hey'), [])
    yield (('hey', 202407260019), [])


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_emoji_and_guild_id_and_id(input_value, extra):
    """
    Tests whether ``get_emoji_and_guild_id_and_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    extra : `list<object>`
        Additional objects to keep in the cache.
    
    Returns
    -------
    output : `(None | Emoji, int, int)`
    
    Raises
    ------
    TypeError
    """
    return get_emoji_and_guild_id_and_id(input_value)
