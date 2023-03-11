import vampytest

from ..fields import put_revoked_into


def test__put_revoked_into():
    """
    Tests whether ``put_revoked_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'revoked': False}),
        (True, False, {'revoked': True}),
    ):
        data = put_revoked_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
