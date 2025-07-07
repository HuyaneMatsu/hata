import vampytest

from ....guild import GuildFeature

from ..sku_enhancement_guild import SKUEnhancementGuild

from .test__SKUEnhancementGuild__constructor import _assert_fields_set


def test__SKUEnhancementGuild__copy():
    """
    Tests whether ``SKUEnhancementGuild.copy`` works as intended.
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
    copy = sku_enhancement_guild.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(sku_enhancement_guild, copy)
    vampytest.assert_eq(sku_enhancement_guild, copy)


def test__SKUEnhancementGuild__copy_with__no_fields():
    """
    Tests whether ``SKUEnhancementGuild.copy_with`` works as intended.
    
    Case: No fields given.
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
    copy = sku_enhancement_guild.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(sku_enhancement_guild, copy)
    vampytest.assert_eq(sku_enhancement_guild, copy)


def test__SKUEnhancementGuild__copy_with__all_fields():
    """
    Tests whether ``SKUEnhancementGuild.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_additional_emoji_slots = 12
    old_additional_soundboard_sound_slots = 13
    old_additional_sticker_slots = 14
    old_features = [GuildFeature.animated_icon]
    
    new_additional_emoji_slots = 20
    new_additional_soundboard_sound_slots = 21
    new_additional_sticker_slots = 22
    new_features = [GuildFeature.animated_banner]
    
    sku_enhancement_guild = SKUEnhancementGuild(
        additional_emoji_slots = old_additional_emoji_slots,
        additional_soundboard_sound_slots = old_additional_soundboard_sound_slots,
        additional_sticker_slots = old_additional_sticker_slots,
        features = old_features,
    )
    copy = sku_enhancement_guild.copy_with(
        additional_emoji_slots = new_additional_emoji_slots,
        additional_soundboard_sound_slots = new_additional_soundboard_sound_slots,
        additional_sticker_slots = new_additional_sticker_slots,
        features = new_features,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(sku_enhancement_guild, copy)
    
    vampytest.assert_eq(copy.additional_emoji_slots, new_additional_emoji_slots)
    vampytest.assert_eq(copy.additional_soundboard_sound_slots, new_additional_soundboard_sound_slots)
    vampytest.assert_eq(copy.additional_sticker_slots, new_additional_sticker_slots)
    vampytest.assert_eq(copy.features, tuple(new_features))
