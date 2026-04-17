import vampytest

from ...emoji import Emoji

from ..request_helpers import get_emoji_guild_id_and_id


def _iter_options__passing():
    emoji_id = 202407260000
    guild_id = 202407260001
    
    yield (
        (guild_id, emoji_id),
        (guild_id, emoji_id),
    )
    
    emoji_id = 202407260002
    guild_id = 202407260003
    
    yield (
        (str(guild_id), str(emoji_id)),
        (guild_id, emoji_id),
    )
    
    emoji_id = 202407260004
    guild_id = 202407260005
    
    yield (
        Emoji.precreate(emoji_id, guild_id = guild_id),
        (guild_id, emoji_id),
    )
    
    
    emoji_id = 202407260006
    guild_id = 0
    
    yield (
        Emoji.precreate(emoji_id, guild_id = guild_id),
        (guild_id, emoji_id),
    )


def _iter_options__type_error():
    yield None
    yield 12.6
    yield ((202407260007, 'hey'),)
    yield (('hey', 202407260008),)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_emoji_guild_id_and_id(input_value):
    """
    Tests whether ``get_emoji_guild_id_and_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `(int, int)`
    
    Raises
    ------
    TypeError
    """
    return get_emoji_guild_id_and_id(input_value)
