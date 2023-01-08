import vampytest

from ..fields import put_require_colons_into


def test__put_require_colons_into():
    """
    Tests whether ``put_require_colons_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (True, False, {}),
        (True, True, {'require_colons': True}),
        (False, False, {'require_colons': False}),
    ):
        data = put_require_colons_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
