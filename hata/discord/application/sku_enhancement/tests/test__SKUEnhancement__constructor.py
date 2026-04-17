import vampytest

from ...sku_enhancement_guild import SKUEnhancementGuild

from ..sku_enhancement import SKUEnhancement


def _assert_fields_set(sku_enhancement):
    """
    Asserts whether all fields of the given SKU enhancement are set.
    
    Parameters
    ----------
    sku_enhancement : ``SKUEnhancement``
    """
    vampytest.assert_instance(sku_enhancement, SKUEnhancement)
    vampytest.assert_instance(sku_enhancement.boost_cost, int)
    vampytest.assert_instance(sku_enhancement.guild, SKUEnhancementGuild, nullable = True)
    vampytest.assert_instance(sku_enhancement.purchase_limit, int)


def test__SKUEnhancement__new__no_fields():
    """
    Tests whether ``SKUEnhancement.__new__`` works as intended.
    
    Case: no fields given.
    """
    sku_enhancement = SKUEnhancement()
    _assert_fields_set(sku_enhancement)


def test__SKUEnhancement__new__all_fields():
    """
    Tests whether ``SKUEnhancement.__new__`` works as intended.
    
    Case: all fields given.
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
    _assert_fields_set(sku_enhancement)
    
    vampytest.assert_eq(sku_enhancement.boost_cost, boost_cost)
    vampytest.assert_eq(sku_enhancement.guild, guild)
    vampytest.assert_eq(sku_enhancement.purchase_limit, purchase_limit)
