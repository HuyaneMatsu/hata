import vampytest

from ...sku_enhancement import SKUEnhancement

from ..fields import validate_enhancement


def _iter_options__passing():
    sku_enhancement = SKUEnhancement(
        boost_cost = 50,
    )
    
    yield None, None
    yield sku_enhancement, sku_enhancement


def _iter_options__type_error():
    yield 12.6
    yield '12'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_enhancement(input_value):
    """
    Tests whether `validate_enhancement` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : ``None | SKUEnhancement``
    
    Raises
    ------
    TypeError
    """
    output = validate_enhancement(input_value)
    vampytest.assert_instance(output, SKUEnhancement, nullable = True)
    return output
