import vampytest

from ....embed import EmbedType

from ..fields import put_embed_types


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'embed_type': [],
        },
    )
    
    yield (
        (
            EmbedType.gift,
            EmbedType.rich,
        ),
        False,
        {
            'embed_type': [
                EmbedType.gift.value,
                EmbedType.rich.value,
            ],
        },
    )
    
    yield (
        (
            EmbedType.gift,
            EmbedType.rich,
        ),
        True,
        {
            'embed_type': [
                EmbedType.gift.value,
                EmbedType.rich.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_embed_types(input_value, defaults):
    """
    Tests whether ``put_embed_types`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<EmbedType>``
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_embed_types(input_value, {}, defaults)
