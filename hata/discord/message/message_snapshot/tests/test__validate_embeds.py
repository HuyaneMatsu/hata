import vampytest

from ....embed import Embed

from ..fields import validate_embeds


def _iter_options__passing():
    embed_0 = Embed('Hell')
    embed_1 = Embed('Rose')
    
    yield None, None
    yield [], None
    yield [embed_0], (embed_0,)
    yield [embed_0, embed_1], (embed_0, embed_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_embeds(input_value):
    """
    Tests whether ``validate_embeds`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | tuple<Embed>``
    
    Raises
    ------
    TypeError
    """
    output = validate_embeds(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output   
