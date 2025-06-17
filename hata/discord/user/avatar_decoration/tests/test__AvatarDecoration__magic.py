from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType

from ..avatar_decoration import AvatarDecoration


def test__AvatarDecoration__repr():
    """
    Tests whether ``AvatarDecoration.__repr__`` works as intended.
    """
    asset = Icon(IconType.static, 12)
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_id = 202310160008
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        expires_at = expires_at,
        sku_id = sku_id,
    )
    
    output = repr(avatar_decoration)
    vampytest.assert_instance(output, str)


def test__AvatarDecoration__hash():
    """
    Tests whether ``AvatarDecoration.__hash__`` works as intended.
    """
    asset = Icon(IconType.static, 12)
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_id = 202310160007
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        expires_at = expires_at,
        sku_id = sku_id,
    )
    
    output = hash(avatar_decoration)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    asset = Icon(IconType.static, 12)
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_id = 202310160006
    
    keyword_parameters = {
        'asset': asset,
        'expires_at': expires_at,
        'sku_id': sku_id,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'asset': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'expires_at': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sku_id': 0,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__AvatarDecoration__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``AvatarDecoration.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    avatar_decoration_0 = AvatarDecoration(**keyword_parameters_0)
    avatar_decoration_1 = AvatarDecoration(**keyword_parameters_1)
    
    output = avatar_decoration_0 == avatar_decoration_1
    vampytest.assert_instance(output, bool)
    return output
