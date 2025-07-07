import vampytest

from ....guild import GuildFeature

from ..sku_enhancement_guild import SKUEnhancementGuild


def _assert_fields_set(sku_enhancement_guild):
    """
    Asserts whether all fields of the given SKU enhancement guild are set.
    
    Parameters
    ----------
    sku_enhancement_guild : ``SKUEnhancementGuild``
    """
    vampytest.assert_instance(sku_enhancement_guild, SKUEnhancementGuild)
    vampytest.assert_instance(sku_enhancement_guild.additional_emoji_slots, int)
    vampytest.assert_instance(sku_enhancement_guild.additional_soundboard_sound_slots, int)
    vampytest.assert_instance(sku_enhancement_guild.additional_sticker_slots, int)
    vampytest.assert_instance(sku_enhancement_guild.features, tuple, nullable = True)


def test__SKUEnhancementGuild__new__no_fields():
    """
    Tests whether ``SKUEnhancementGuild.__new__`` works as intended.
    
    Case: no fields given.
    """
    sku_enhancement_guild = SKUEnhancementGuild()
    _assert_fields_set(sku_enhancement_guild)


def test__SKUEnhancementGuild__new__all_fields():
    """
    Tests whether ``SKUEnhancementGuild.__new__`` works as intended.
    
    Case: all fields given.
    """
    additional_emoji_slots = 12
    additional_soundboard_sound_slots = 13
    additional_sticker_slots = 14
    features = [GuildFeature.animated_icon]
    
    sku_enhancement_guild = SKUEnhancementGuild(
        additional_emoji_slots = additional_emoji_slots,
        additional_soundboard_sound_slots = additional_soundboard_sound_slots,
        additional_sticker_slots = additional_sticker_slots,
        features = features,
    )
    _assert_fields_set(sku_enhancement_guild)
    
    vampytest.assert_eq(sku_enhancement_guild.additional_emoji_slots, additional_emoji_slots)
    vampytest.assert_eq(sku_enhancement_guild.additional_soundboard_sound_slots, additional_soundboard_sound_slots)
    vampytest.assert_eq(sku_enhancement_guild.additional_sticker_slots, additional_sticker_slots)
    vampytest.assert_eq(sku_enhancement_guild.features, tuple(features))
