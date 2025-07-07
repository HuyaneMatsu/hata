import vampytest

from ...sku_enhancement import SKUEnhancement

from ..fields import parse_enhancement


def _iter_options():
    sku_enhancement = SKUEnhancement(
        boost_cost = 50,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'powerup_metadata': None,
        },
        None,
    )
    
    yield (
        {
            'powerup_metadata': sku_enhancement.to_data(),
        },
        sku_enhancement,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_enhancement(input_data):
    """
    Tests whether ``parse_enhancement`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | SKUEnhancement``
    """
    output = parse_enhancement(input_data)
    vampytest.assert_instance(output, SKUEnhancement, nullable = True)
    return output
