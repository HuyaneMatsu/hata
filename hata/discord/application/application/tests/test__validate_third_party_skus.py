import vampytest

from ...third_party_sku import ThirdPartySKU

from ..fields import validate_third_party_skus


def test__validate_third_party_skus_0():
    """
    Tests whether ``validate_third_party_skus`` works as intended.
    
    Case: Passing.
    """
    third_party_sku = ThirdPartySKU(distributor = 'Suika')
    
    for input_parameter, expected_output in (
        (None, None),
        ([], None),
        ([third_party_sku], (third_party_sku, ))
    ):
        output = validate_third_party_skus(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_third_party_skus__1():
    """
    Tests whether ``validate_third_party_skus`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        2.3,
        [2.3],
    ):
        with vampytest.assert_raises(TypeError):
            validate_third_party_skus(input_value)
