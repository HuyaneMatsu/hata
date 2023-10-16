import vampytest

from ....bases import Icon, IconType

from ...avatar_decoration import AvatarDecoration

from ..fields import validate_avatar_decoration


def _iter_options():
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160014)
    
    yield (None, None)
    yield (avatar_decoration, avatar_decoration)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_avatar_decoration__passing(input_value):
    """
    Tests whether `validate_avatar_decoration` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | AvatarDecoration`
    """
    return validate_avatar_decoration(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_avatar_decoration__type_error(input_value):
    """
    Tests whether `validate_avatar_decoration` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_avatar_decoration(input_value)
