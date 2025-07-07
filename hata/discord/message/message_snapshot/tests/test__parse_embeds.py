import vampytest

from ....embed import Embed

from ..fields import parse_embeds


def _iter_options():
    embed_0 = Embed('Hell')
    embed_1 = Embed('Rose')
    
    yield {}, None
    
    yield {'message': None}, None
    
    yield {'message': {}}, None
    
    yield (
        {},
        None,
    )
    
    yield (
        {'message': {'embeds': None}},
        None,
    )
    
    yield (
        {'message': {'embeds': [embed_0.to_data()]}},
        (embed_0,),
    )
    
    yield (
        {'message': {'embeds': [embed_0.to_data(), embed_1.to_data()]}},
        (embed_0, embed_1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_embeds(input_data):
    """
    Tests whether ``parse_embeds`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<Embed>``
    """
    output = parse_embeds(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
