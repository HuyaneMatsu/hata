import vampytest

from ...sku_enhancement_guild import SKUEnhancementGuild

from ..sku_enhancement import SKUEnhancement

from .test__SKUEnhancement__constructor import _assert_fields_set


def test__SKUEnhancement__copy():
    """
    Tests whether ``SKUEnhancement.copy`` works as intended.
    """
    boost_cost = 12
    guild = SKUEnhancementGuild(
        additional_emoji_slots = 13,
    )
    purchase_limit = 14
    
    
    sku_enhancement = SKUEnhancement(
        boost_cost = boost_cost,
        guild = guild,
        purchase_limit = purchase_limit,
    )
    copy = sku_enhancement.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(sku_enhancement, copy)
    vampytest.assert_eq(sku_enhancement, copy)


def test__SKUEnhancement__copy_with__no_fields():
    """
    Tests whether ``SKUEnhancement.copy_with`` works as intended.
    
    Case: No fields given.
    """
    boost_cost = 12
    guild = SKUEnhancementGuild(
        additional_emoji_slots = 13,
    )
    purchase_limit = 14
    
    
    sku_enhancement = SKUEnhancement(
        boost_cost = boost_cost,
        guild = guild,
        purchase_limit = purchase_limit,
    )
    copy = sku_enhancement.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(sku_enhancement, copy)
    vampytest.assert_eq(sku_enhancement, copy)


def test__SKUEnhancement__copy_with__all_fields():
    """
    Tests whether ``SKUEnhancement.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_boost_cost = 12
    old_guild = SKUEnhancementGuild(
        additional_emoji_slots = 13,
    )
    old_purchase_limit = 14
    
    new_boost_cost = 20
    new_guild = SKUEnhancementGuild(
        additional_emoji_slots = 21,
    )
    new_purchase_limit = 22
    
    sku_enhancement = SKUEnhancement(
        boost_cost = old_boost_cost,
        guild = old_guild,
        purchase_limit = old_purchase_limit,
    )
    copy = sku_enhancement.copy_with(
        boost_cost = new_boost_cost,
        guild = new_guild,
        purchase_limit = new_purchase_limit,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(sku_enhancement, copy)
    
    vampytest.assert_eq(copy.boost_cost, new_boost_cost)
    vampytest.assert_eq(copy.guild, new_guild)
    vampytest.assert_eq(copy.purchase_limit, new_purchase_limit)
