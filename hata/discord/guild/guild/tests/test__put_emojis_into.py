import vampytest

from ....emoji import Emoji

from ..fields import put_emojis_into


def iter_options():
    emoji_id = 202306090002
    emoji_name = 'Koishi'
    
    emoji = Emoji.precreate(
        emoji_id,
        name = emoji_name,
    )
    
    yield {}, True, {'emojis': []}
    yield {emoji_id: emoji}, True, {'emojis': [emoji.to_data(defaults = True, include_internals = True)]}


@vampytest._(vampytest.call_from(iter_options()).returning_last())
def test__put_emojis_into(input_value, defaults):
    """
    Tests whether ``put_emojis_into`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<int, Emoji>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_emojis_into(input_value, {}, defaults)
