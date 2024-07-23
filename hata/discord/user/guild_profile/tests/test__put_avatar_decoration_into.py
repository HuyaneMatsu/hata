import vampytest

from ....bases import Icon, IconType

from ...avatar_decoration import AvatarDecoration

from ..fields import put_avatar_decoration_into


def _iter_options():
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150001)
    
    yield (None, False, {})
    yield (None, True, {'avatar_decoration_data': None})
    yield (avatar_decoration, False, {'avatar_decoration_data': avatar_decoration.to_data()})
    yield (avatar_decoration, True, {'avatar_decoration_data': avatar_decoration.to_data(defaults = True)})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_avatar_decoration_into(input_value, defaults):
    """
    Tests whether ``put_avatar_decoration_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | AvatarDecoration`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default value should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_avatar_decoration_into(input_value, {}, defaults)
