import vampytest

from ....bases import Icon, IconType

from ..avatar_decoration import AvatarDecoration

from .test__AvatarDecoration__constructor import _check_is_all_fields_set


def test__AvatarDecoration__from_data():
    """
    Tests whether ``AvatarDecoration.from_data`` works as intended.
    """
    asset = Icon(IconType.static, 12)
    sku_id = 202310160005
    
    data = {
        'asset': asset.as_base_16_hash,
            'sku_id': str(sku_id),
    }
    
    avatar_decoration = AvatarDecoration.from_data(data)
    _check_is_all_fields_set(avatar_decoration)
    
    vampytest.assert_eq(avatar_decoration.asset, asset)
    vampytest.assert_eq(avatar_decoration.sku_id, sku_id)


def test__AvatarDecoration__to_data():
    """
    Tests whether ``AvatarDecoration.to_data`` works as intended.
    
    Case: Include defaults.
    """
    asset = Icon(IconType.static, 12)
    sku_id = 20231016004
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        sku_id = sku_id,
    )
    
    vampytest.assert_eq(
        avatar_decoration.to_data(
            defaults = True,
        ),
        {
            'asset': asset.as_base_16_hash,
            'sku_id': str(sku_id),
        },
    )
