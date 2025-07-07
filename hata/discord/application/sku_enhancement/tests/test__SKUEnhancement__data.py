import vampytest

from ...sku_enhancement_guild import SKUEnhancementGuild

from ..sku_enhancement import SKUEnhancement

from .test__SKUEnhancement__constructor import _assert_fields_set


def test__SKUEnhancement__from_data():
    """
    Tests whether ``SKUEnhancement.from_data`` works as intended.
    """
    boost_cost = 12
    guild = SKUEnhancementGuild(
        additional_emoji_slots = 13,
    )
    purchase_limit = 14
    
    data = {
        'boost_price': boost_cost,
        'guild_features': guild.to_data(),
        'purchase_limit': purchase_limit,
    }
    
    sku_enhancement = SKUEnhancement.from_data(data)
    _assert_fields_set(sku_enhancement)
    
    vampytest.assert_eq(sku_enhancement.boost_cost, boost_cost)
    vampytest.assert_eq(sku_enhancement.guild, guild)
    vampytest.assert_eq(sku_enhancement.purchase_limit, purchase_limit)


def test__SKUEnhancement__to_data():
    """
    Tests whether ``SKUEnhancement.to_data`` works as intended.
    
    Case: Include defaults.
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
    
    vampytest.assert_eq(
        sku_enhancement.to_data(
            defaults = True,
        ),
        {
            'boost_price': boost_cost,
            'guild_features': guild.to_data(defaults = True),
            'purchase_limit': purchase_limit,
        },
    )
