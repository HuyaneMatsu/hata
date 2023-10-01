import vampytest

from ..fields import validate_features
from ..preinstanced import SKUFeature


def _iter_options():
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
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_features__0(input_value):
    """
    Tests whether `validate_features` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<SKUFeature>
    """
    return validate_features(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_features__type_error(input_value):
    """
    Tests whether `validate_features` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_features(input_value)
