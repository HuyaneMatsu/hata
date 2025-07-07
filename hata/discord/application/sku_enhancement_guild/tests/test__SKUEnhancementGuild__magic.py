import vampytest

from ....guild import GuildFeature

from ..sku_enhancement_guild import SKUEnhancementGuild


def test__SKUEnhancementGuild__repr():
    """
    Tests whether ``SKUEnhancementGuild.__repr__`` works as intended.
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
    
    output = repr(sku_enhancement_guild)
    vampytest.assert_instance(output, str)


def test__SKUEnhancementGuild__hash():
    """
    Tests whether ``SKUEnhancementGuild.__hash__`` works as intended.
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
    
    output = hash(sku_enhancement_guild)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    additional_emoji_slots = 12
    additional_soundboard_sound_slots = 13
    additional_sticker_slots = 14
    features = [GuildFeature.animated_icon]
    
    keyword_parameters = {
        'additional_emoji_slots': additional_emoji_slots,
        'additional_soundboard_sound_slots': additional_soundboard_sound_slots,
        'additional_sticker_slots': additional_sticker_slots,
        'features': features,
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
            'additional_emoji_slots': 20,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'additional_soundboard_sound_slots': 21,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'additional_sticker_slots': 22,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'features': [GuildFeature.animated_banner],
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__SKUEnhancementGuild__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``SKUEnhancementGuild.__eq__`` works as intended.
    
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
    sku_enhancement_guild_0 = SKUEnhancementGuild(**keyword_parameters_0)
    sku_enhancement_guild_1 = SKUEnhancementGuild(**keyword_parameters_1)
    
    output = sku_enhancement_guild_0 == sku_enhancement_guild_1
    vampytest.assert_instance(output, bool)
    return output
