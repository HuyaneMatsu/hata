import vampytest

from ...third_party_sku import ThirdPartySKU

from ..fields import parse_third_party_skus


def test__parse_third_party_skus():
    """
    Tests whether ``parse_third_party_skus`` works as intended.
    """
    third_party_sku = ThirdPartySKU(distributor = 'Suika')
    
    for input_data, expected_output in (
        ({}, None),
        ({'third_party_skus': None}, None),
        ({'third_party_skus': []}, None),
        (
            {'third_party_skus': [third_party_sku.to_data(defaults = True)]},
            (third_party_sku, )
        )
    ):
        output = parse_third_party_skus(input_data)
        vampytest.assert_eq(output, expected_output)
