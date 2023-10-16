import vampytest

from ....bases import Icon, IconType

from ..avatar_decoration import AvatarDecoration


def test__AvatarDecoration__repr():
    """
    Tests whether ``AvatarDecoration.__repr__`` works as intended.
    """
    asset = Icon(IconType.static, 12)
    sku_id = 202310160008
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        sku_id = sku_id,
    )
    
    vampytest.assert_instance(repr(avatar_decoration), str)


def test__AvatarDecoration__hash():
    """
    Tests whether ``AvatarDecoration.__hash__`` works as intended.
    """
    asset = Icon(IconType.static, 12)
    sku_id = 202310160007
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        sku_id = sku_id,
    )
    
    vampytest.assert_instance(hash(avatar_decoration), int)


def test__AvatarDecoration__eq():
    """
    Tests whether ``AvatarDecoration.__eq__`` works as intended.
    """
    asset = Icon(IconType.static, 12)
    sku_id = 202310160006
    
    keyword_parameters = {
        'asset': asset,
        'sku_id': sku_id,
    }
    
    avatar_decoration = AvatarDecoration(**keyword_parameters)
    
    vampytest.assert_eq(avatar_decoration, avatar_decoration)
    vampytest.assert_ne(avatar_decoration, object())
    
    for field_name, field_value in (
        ('asset', None),
        ('sku_id', None),
    ):
        test_avatar_decoration = AvatarDecoration(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(avatar_decoration, test_avatar_decoration)
