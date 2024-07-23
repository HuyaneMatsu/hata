import vampytest

from ....bases import Icon, IconType

from ...avatar_decoration import AvatarDecoration

from ..fields import validate_avatar_decoration


def _iter_options__passing():
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150002)
    
    yield (None, None)
    yield (avatar_decoration, avatar_decoration)


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_avatar_decoration(input_value):
    """
    Tests whether `validate_avatar_decoration` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | AvatarDecoration`
    
    Raises
    ------
    TypeError
    """
    return validate_avatar_decoration(input_value)
