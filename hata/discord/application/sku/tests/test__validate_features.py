import vampytest

from ..fields import validate_features
from ..preinstanced import SKUFeature


def _iter_options__passing():
    yield None, None
    yield [], None
    yield SKUFeature.single_player, (SKUFeature.single_player, )
    yield SKUFeature.single_player.value, (SKUFeature.single_player, )
    yield [SKUFeature.single_player], (SKUFeature.single_player, )
    yield [SKUFeature.single_player.value], (SKUFeature.single_player, )
    yield (
        [SKUFeature.single_player, SKUFeature.pvp],
        (SKUFeature.single_player, SKUFeature.pvp,),
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_features(input_value):
    """
    Tests whether `validate_features` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<SKUFeature>`
    
    Raises
    ------
    TypeError
    """
    output = validate_features(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
