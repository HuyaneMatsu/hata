import vampytest

from ...sku_enhancement import SKUEnhancement

from ..fields import put_enhancement


def _iter_options():
    sku_enhancement = SKUEnhancement(
        boost_cost = 50,
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'powerup_metadata': None,
        },
    )
    
    yield (
        sku_enhancement,
        False,
        {
            'powerup_metadata': sku_enhancement.to_data(defaults = False)
        },
    )
    
    yield (
        sku_enhancement,
        True,
        {
            'powerup_metadata': sku_enhancement.to_data(defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_enhancement(input_value, defaults):
    """
    Tests whether ``put_enhancement`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | SKUEnhancement``
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_enhancement(input_value, {}, defaults)
