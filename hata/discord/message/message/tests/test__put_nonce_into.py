import vampytest

from ..fields import put_nonce_into


def test__put_nonce_into():
    """
    Tests whether ``put_nonce_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'nonce': None}),
        ('Orin', False, {'nonce': 'Orin'}),
    ):
        data = put_nonce_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
