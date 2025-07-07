import vampytest

from ....embed import Embed

from ..fields import put_embeds


def _iter_options():
    embed_0 = Embed('Hell')
    embed_1 = Embed('Rose')
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'message': {
                'embeds': [],
            },
        },
    )
    
    yield (
        (embed_0, embed_1),
        False,
        {
            'message': {
                'embeds': [
                    embed_0.to_data(defaults = False),
                    embed_1.to_data(defaults = False),
                ],
            },
        },
    )
    
    yield (
        (embed_0, embed_1),
        True,
        {
            'message': {
                'embeds': [
                    embed_0.to_data(defaults = True),
                    embed_1.to_data(defaults = True),
                ],
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_embeds(input_value, defaults):
    """
    Tests whether ``put_embeds`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<Embed>``
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_embeds(input_value, {}, defaults)
