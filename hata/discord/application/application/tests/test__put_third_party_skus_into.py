import vampytest

from ...third_party_sku import ThirdPartySKU

from ..fields import put_third_party_skus_into


def test__put_third_party_skus_into():
    """
    Tests whether ``put_third_party_skus_into`` works as intended.
    
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
        data = put_third_party_skus_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
