import vampytest

from ..fields import put_sku


def test__put_sku():
    """
    Tests whether ``put_sku`` works as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'sku': ''}),
        ('a', False, {'sku': 'a'}),
    ):
        data = put_sku(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
