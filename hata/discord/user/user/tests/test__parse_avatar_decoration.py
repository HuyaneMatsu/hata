import vampytest

from ....bases import Icon, IconType

from ...avatar_decoration import AvatarDecoration

from ..fields import parse_avatar_decoration


def _iter_options():
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160012)
    
    yield ({}, None)
    yield ({'avatar_decoration_data': None}, None)
    yield ({'avatar_decoration_data': avatar_decoration.to_data()}, avatar_decoration)
    


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_avatar_decoration(input_data):
    """
    Tests whether ``parse_avatar_decoration`` works as intended.
    
    Parameters
    ----------
    input_data : dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | AvatarDecoration`
    """
    return parse_avatar_decoration(input_data)
