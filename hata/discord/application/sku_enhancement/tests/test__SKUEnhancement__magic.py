import vampytest

from ...sku_enhancement_guild import SKUEnhancementGuild

from ..sku_enhancement import SKUEnhancement


def test__SKUEnhancement__repr():
    """
    Tests whether ``SKUEnhancement.__repr__`` works as intended.
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
    
    output = repr(sku_enhancement)
    vampytest.assert_instance(output, str)


def test__SKUEnhancement__hash():
    """
    Tests whether ``SKUEnhancement.__hash__`` works as intended.
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
    
    output = hash(sku_enhancement)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    boost_cost = 12
    guild = SKUEnhancementGuild(
        additional_emoji_slots = 13,
    )
    purchase_limit = 14
    
    keyword_parameters = {
        'boost_cost': boost_cost,
        'guild': guild,
        'purchase_limit': purchase_limit,
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
            'boost_cost': 20,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild': SKUEnhancementGuild(
                additional_emoji_slots = 21,
            ),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'purchase_limit': 22,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__SKUEnhancement__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``SKUEnhancement.__eq__`` works as intended.
    
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
    sku_enhancement_0 = SKUEnhancement(**keyword_parameters_0)
    sku_enhancement_1 = SKUEnhancement(**keyword_parameters_1)
    
    output = sku_enhancement_0 == sku_enhancement_1
    vampytest.assert_instance(output, bool)
    return output
