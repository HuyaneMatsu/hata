import vampytest

from ..fields import put_require_colons


def test__put_require_colons():
    """
    Tests whether ``put_require_colons`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (True, False, {}),
        (True, True, {'require_colons': True}),
        (False, False, {'require_colons': False}),
    ):
        data = put_require_colons(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
