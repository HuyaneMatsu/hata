import vampytest

from ..fields import put_sku_into


def test__put_sku_into():
    """
    Tests whether ``put_sku_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'sku': ''}),
        ('a', False, {'sku': 'a'}),
    ):
        data = put_sku_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
