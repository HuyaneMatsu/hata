import vampytest

from ...third_party_sku import ThirdPartySKU

from ..fields import put_third_party_skus


def test__put_third_party_skus():
    """
    Tests whether ``put_third_party_skus`` works as intended.
    
    Case: include internals.
    """
    third_party_sku = ThirdPartySKU(distributor = 'Suika')
    
    for input_, defaults, expected_output in (
        (None, True, {'third_party_skus': []}),
        (
            [third_party_sku],
            False,
            {'third_party_skus': [third_party_sku.to_data(defaults = True)]}
        ),
    ):
        data = put_third_party_skus(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
