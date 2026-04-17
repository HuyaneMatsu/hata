import vampytest

from ....embed import EmbedType

from ..fields import parse_embed_types


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'embed_type': None,
        },
        None,
    )
    
    yield (
        {
            'embed_type': [],
        },
        None,
    )
    
    yield (
        {
            'embed_type': [
                EmbedType.gift.value,
                EmbedType.rich.value,
            ],
        },
        (
            EmbedType.gift,
            EmbedType.rich,
        ),
    )
    
    yield (
        {
            'embed_type': [
                EmbedType.rich.value,
                EmbedType.gift.value,
            ],
        },
        (
            EmbedType.gift,
            EmbedType.rich,
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_embed_types(input_data):
    """
    Tests whether ``parse_embed_types`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output :  ``None | tuple<EmbedType>``
    """
    output = parse_embed_types(input_data)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, EmbedType)
    
    return output
