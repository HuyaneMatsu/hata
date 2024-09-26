import vampytest

from ...sticker import Sticker

from ..fields import validate_stickers


def _iter_options__passing():
    sticker_0 = Sticker.precreate(202301050018, name = 'just')
    sticker_1 = Sticker.precreate(202301050019, name = 'flowering')
    
    yield None, None
    yield [], None
    yield [sticker_0, sticker_1], frozenset((sticker_0, sticker_1))


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_stickers(input_value):
    """
    Tests whether ``validate_stickers`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | frozenset<Sticker>`
    
    Raises
    ------
    TypeError
    """
    output = validate_stickers(input_value)
    vampytest.assert_instance(output, frozenset, nullable = True)
    return output
