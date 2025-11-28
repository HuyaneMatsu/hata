import vampytest

from ....guild import GuildFeature

from ..sku_enhancement_guild import SKUEnhancementGuild

from .test__SKUEnhancementGuild__constructor import _assert_fields_set


def test__SKUEnhancementGuild__from_data():
    """
    Tests whether ``SKUEnhancementGuild.from_data`` works as intended.
    """
    additional_emoji_slots = 12
    additional_soundboard_sound_slots = 13
    additional_sticker_slots = 14
    features = [GuildFeature.icon_animated]
    
    data = {
        'additional_emoji_slots': additional_emoji_slots,
        'additional_sound_slots': additional_soundboard_sound_slots,
        'additional_sticker_slots': additional_sticker_slots,
        'features': [feature.value for feature in features],
    }
    
    sku_enhancement_guild = SKUEnhancementGuild.from_data(data)
    _assert_fields_set(sku_enhancement_guild)
    
    vampytest.assert_eq(sku_enhancement_guild.additional_emoji_slots, additional_emoji_slots)
    vampytest.assert_eq(sku_enhancement_guild.additional_soundboard_sound_slots, additional_soundboard_sound_slots)
    vampytest.assert_eq(sku_enhancement_guild.additional_sticker_slots, additional_sticker_slots)
    vampytest.assert_eq(sku_enhancement_guild.features, tuple(features))


def test__SKUEnhancementGuild__to_data():
    """
    Tests whether ``SKUEnhancementGuild.to_data`` works as intended.
    
    Case: Include defaults.
    """
    additional_emoji_slots = 12
    additional_soundboard_sound_slots = 13
    additional_sticker_slots = 14
    features = [GuildFeature.icon_animated]
    
    sku_enhancement_guild = SKUEnhancementGuild(
        additional_emoji_slots = additional_emoji_slots,
        additional_soundboard_sound_slots = additional_soundboard_sound_slots,
        additional_sticker_slots = additional_sticker_slots,
        features = features,
    )
    
    vampytest.assert_eq(
        sku_enhancement_guild.to_data(
            defaults = True,
        ),
        {
            'additional_emoji_slots': additional_emoji_slots,
            'additional_sound_slots': additional_soundboard_sound_slots,
            'additional_sticker_slots': additional_sticker_slots,
            'features': [feature.value for feature in features],
        },
    )
